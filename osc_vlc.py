"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import vlc360_qt as vlc360
import time
import v_threading as vt
import logging

from pythonosc import dispatcher
from pythonosc import osc_server

logging.basicConfig(filename='osc_vlc.log', level=logging.DEBUG, format = '%(asctime)s %(message)s')
class OscServer(vlc360.Player):
    def start_osc(self):
        logging.info("Setting OscServer parameters")
        self.parser = argparse.ArgumentParser()
        # self.parser.add_argument("--ip",
        #                    default="127.0.0.1", help="The ip to listen on")
        self.parser.add_argument("--ip", default="192.168.248.137", help="The ip to listen on")
        self.parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
        self.args = self.parser.parse_args()

        self.dispatcher = dispatcher.Dispatcher()
        self.messages = []
        self.pan_threads = []
        self.fade_threads = []
        self.hue_fade_threads = []

    def print_volume_handler(unused_addr, args, volume):
        print("[{0}] ~ {1}".format(args[0], volume))

    def print_compute_handler(unused_addr, args, volume):
        try:
            print("[{0}] ~ {1}".format(args[0], args[1](volume)))
        except ValueError:
            pass

    def add_message(unused_addr, args, volume):
        print("args :", args)
        print("volume :", volume)

    def play_loop(self, args, status):
        if status == True:
            # self.m.set_loop(self.mediaplayer.player, self.m, True)
            vlc360.vlc.libvlc_vlm_set_loop(self.player, self.m, True)

    def load_file(self, args, file, coords=[0, 0, 0, 0]):
        """
        Loads a new file with optional specified coordinates.
        :param args:
        :param file: Video file
        :param coords: Orientation variables: yaw, pitch, roll, fov
        :return:
        """
        logging.info("Loading file {} at coords : {}".format(str(file), str(coords)))
        print("log?")
        # i = vlc360.vlc.Instance()
        self.m = self.instance.media_new(str(file))

        yaw = coords[0]
        pitch = coords[1]
        roll = coords[2]
        field_of_view = coords[3]
        v = vlc360.vlc.VideoViewpoint(yaw, pitch, roll, field_of_view)
        print(file, coords, v)

        print(self.m)
        self.m.get_mrl()

        # self.player.mediaplayer.video_update_viewpoint(v, True)

        self.player.mediaplayer.set_media(self.m)
        self.player.mediaplayer.play()
        self.player.mediaplayer.video_update_viewpoint(v, True)
        # self.player.mediaplayer.next_frame()
        # This should move the video the next frame
        # which should update the viewpoint. However, it currently displays a black frame only.

    def adjust_yaw(self, args, yaw):
        print("YAW!")
        v = vlc360.vlc.VideoViewpoint(yaw)
        self.player.mediaplayer.video_update_viewpoint(v, True)

    def pan_loop(self):
        # while not self.exit_flag.wait(timeout=0.01):
        #     self.player.mediaplayer.video_update_viewpoint(self.player.mediaplayer.v, False)
        if len(self.pan_threads) > 0:
            print(len(self.pan_threads))
            while self.pan_threads[len(self.pan_threads) - 1].stopped != True:
                time.sleep(0.01)
                self.player.mediaplayer.video_update_viewpoint(self.player.mediaplayer.v, False)

    def pan(self, args, coords=[0, 0, 0, 0]):
        """
        Continuously pans around in all directions at the increments specified
        :param args: n/a
        :param coords: Orientation variables: yaw, pitch, roll, fov. Default of 0 means stopped
        :return:
        """
        logging.info("Starting pan at {}".format(str(coords)))

        yaw = coords[0]
        pitch = coords[1]
        roll = coords[2]
        field_of_view = coords[3]
        v = vlc360.vlc.VideoViewpoint(yaw, pitch, roll, field_of_view)
        # print("v :", v)
        self.player.mediaplayer.v = v

        if len(self.pan_threads) == 0:
            # self.pan_loopThread = threading.Thread(target=self.playloop(v))
            self.pan_loopThread = vt.v_thread(target=self.pan_loop)
            self.pan_threads.append(self.pan_loopThread)
            self.pan_threads[0].start()

        # else:
        # self.player.mediaplayer.video_update_viewpoint(v, False)

    def pov(self, args, coords=[0, 0, 0, 0]):
        """
        Sets a playing video to the specified coordinates
        :param args: n/a
        :param coords: Orientation variables: yaw, pitch, roll, fov
        :return:
        """
        logging.info("Changing viewpoint to {}".format(coords))
        print("pov")
        yaw = coords[0]
        pitch = coords[1]
        roll = coords[2]
        field_of_view = coords[3]
        v = vlc360.vlc.VideoViewpoint(yaw, pitch, roll, field_of_view)
        print("v :", v)
        self.player.mediaplayer.video_update_viewpoint(v, True)

    def brightness(self, args, level):
        print("Brightness")
        logging.info("Brightness set to {}".format(level))
        self.player.mediaplayer.video_set_adjust_int(vlc360.vlc.VideoAdjustOption.Enable, 1)
        self.player.mediaplayer.video_set_adjust_float(vlc360.vlc.VideoAdjustOption.Brightness, level)

        if self.player.mediaplayer.video_get_adjust_float(vlc360.vlc.VideoAdjustOption.Saturation) > 0:
            self.player.mediaplayer.video_set_adjust_float(vlc360.vlc.VideoAdjustOption.Saturation, level)

    def saturation(self, args, level):
        self.player.mediaplayer.video_set_adjust_int(vlc360.vlc.VideoAdjustOption.Enable, 1)
        self.player.mediaplayer.video_set_adjust_float(vlc360.vlc.VideoAdjustOption.Saturation, level)

    def hue(self, args, level):
        self.player.mediaplayer.video_set_adjust_int(vlc360.vlc.VideoAdjustOption.Enable, 1)
        self.player.mediaplayer.video_set_adjust_float(vlc360.vlc.VideoAdjustOption.Hue, level)

    def hue_fade(self, args, level):
        self.hue_fade_level = level
        self.player.mediaplayer.video_set_adjust_int(vlc360.vlc.VideoAdjustOption.Enable, 1)
        l = len(self.hue_fade_threads)
        self.hue_loopThread = vt.v_thread(target=self.hue_fade_loop)
        self.hue_fade_threads.append(self.hue_loopThread)
        self.hue_fade_threads[l].start()

    def hue_fade_loop(self):
        c_lev = self.player.mediaplayer.video_get_adjust_int(vlc360.vlc.VideoAdjustOption.Hue)
        while not self.exit_flag.wait(timeout=0.01):
            if c_lev < 360:
                c_lev += 2
            else:
                c_lev = -360
            self.player.mediaplayer.video_set_adjust_float(vlc360.vlc.VideoAdjustOption.Hue, c_lev)
    def fade(self, args, level):
        # print("args, level :", args, level)
        logging.info("Fading to {}".format(level))
        self.fade_level = level
        self.player.mediaplayer.video_set_adjust_int(vlc360.vlc.VideoAdjustOption.Enable, 1)
        l = len(self.fade_threads)
        self.fade_loopThread = vt.v_thread(target=self.fade_loop)
        self.fade_threads.append(self.fade_loopThread)
        self.fade_threads[l].start()

    def fade_loop(self):
        logging.info("Entering fade loop")
        level = self.fade_level
        c_lev = self.player.mediaplayer.video_get_adjust_float(vlc360.vlc.VideoAdjustOption.Brightness)
        while not self.exit_flag.wait(timeout=0.01):
            if c_lev > level:
                # print("too bright c, l :", c_lev, level)
                c_lev -= .05
                self.player.mediaplayer.video_set_adjust_float(vlc360.vlc.VideoAdjustOption.Brightness, c_lev)
                self.player.mediaplayer.video_set_adjust_float(vlc360.vlc.VideoAdjustOption.Saturation, c_lev)
                if c_lev <= level:
                    l = len(self.fade_threads)
                    self.fade_threads[l - 1].stop()
                    self.fade_threads = self.fade_threads[:-1]
                    break

            elif c_lev < level:
                # print("too dark c, l :", c_lev, level)
                c_lev += .05
                self.player.mediaplayer.video_set_adjust_float(vlc360.vlc.VideoAdjustOption.Brightness, c_lev)
                self.player.mediaplayer.video_set_adjust_float(vlc360.vlc.VideoAdjustOption.Saturation, c_lev)
                if c_lev >= level:
                    l = len(self.fade_threads)
                    self.fade_threads[l - 1].stop()
                    self.fade_threads = self.fade_threads[:-1]
                    break
            else:
                break

    def play(self, file, args):
        """
        Deprecated - see load_file, an polymorphic version of the same function
        :param file: The file to play
        :param args: n/a
        :return:
        """
        i = vlc360.vlc.Instance()
        m = i.media_new('V1.mp4')
        m.get_mrl()
        self.player.mediaplayer.set_media(m)
        self.player.mediaplayer.play()

    def pause(self, args, null):
        logging.info("Pausing")
        if self.player.mediaplayer.get_state() == vlc360.vlc.State.Playing:
            self.player.mediaplayer.pause()
        # else:
        # self.player.mediaplayer.pause()
        # print(self.player.mediaplayer.get_state())

    def report_back(self, args, volume):
        if self.messages == True:
            return self.messages
        else:
            return False

    def watch_end(self, args, null):
        logging.info("Entering watch end loop")
        self.watch_thread = vt.v_thread(target=self.check_end)
        self.watch_thread.start()

    def prep_end(self, null):
        logging.info("The mediaplayer has stopped. - EventManager")
        print("It's done.")

    def nothing_special(self):
        print("nothing special - EventManager")
        # fps = self.player.mediaplayer.get_fps()
        # print("FPS :", fps)


    def check_end(self):
        logging.info("Entering check_end loop")
        end_fade = 0
        while not self.exit_flag.wait(timeout=0.01):
            total_time = self.m.get_duration()
            current_time = self.player.mediaplayer.get_time()
            # print("Current, total :", current_time, total_time)
            if (total_time - current_time) < 500:
                if end_fade ==0:
                    end_fade = 1
                    self.fade(0, -1.0)
                    # time.sleep(.5)
                while len(self.pan_threads) > 0:
                    l = len(self.pan_threads)
                    logging.info("Closing pan_threads current #{}".format(str(l)))
                    self.pan_threads[l - 1].stop()
                    self.pan_threads = self.pan_threads[:-1]

                while len(self.fade_threads) > 0:
                    l = len(self.fade_threads)
                    logging.info("Closing fade_threads current #{}".format(str(l)))
                    self.fade_threads[l - 1].stop()
                    self.fade_threads = self.fade_threads[:-1]
                self.watch_thread.stop()


            # if self.player.mediaplayer.get_position() > .98:
            #    self.fade(0, -1.0)

    def start_server(self):
        self.dispatcher.map("/filter", print)
        self.dispatcher.map("/pause", self.pause)

        self.dispatcher.map("/volume", self.print_volume_handler, "Volume")
        self.dispatcher.map("/logvolume", self.print_compute_handler, "Log volume", math.log)
        self.dispatcher.map("/vlc/file", self.load_file)
        self.dispatcher.map("/vlc/pov", self.pov)
        self.dispatcher.map("/vlc/pan", self.pan)
        self.dispatcher.map("/vlc/brightness", self.brightness)
        self.dispatcher.map("/vlc/yaw", self.adjust_yaw)
        self.dispatcher.map("/vlc/fade", self.fade)
        self.dispatcher.map("/vlc/saturation", self.saturation)
        self.dispatcher.map("/vlc/watch_end", self.watch_end)
        self.dispatcher.map("/vlc/hue", self.hue)
        self.dispatcher.map("/vlc/loop", self.play_loop)
        self.dispatcher.map("/vlc/hue_fade", self.hue_fade)

        self.server = osc_server.ThreadingOSCUDPServer(
            (self.args.ip, self.args.port), self.dispatcher)
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()

    def startVlc(self):
        logging.info("Calling the qt_VLC Player")
        """
        Start the VLC player instance
        :return:
        """

        # self.instance = vlc360.vlc.Instance()
        # self.player = self.instance.media_player_new()

        self.player = vlc360.Player()
        # self.event_man = self.player.event_manager()
        self.event_man = vlc360.vlc.libvlc_media_player_event_manager(self.player.mediaplayer)
        self.event_man.event_attach(vlc360.vlc.EventType.MediaPlayerStopped, self.prep_end)
        # self.event_man.event_attach(vlc360.vlc.EventType.MediaPlayerPlaying, self.nothing_special)
        # Unsure of exactly how to call callbacks

        self.player.show()
        # self.player.showFullScreen()

        self.player.resize(1024, 768)
        if vlc360.sys.argv[1:]:
            self.player.OpenFile(vlc360.sys.argv[1])

        """
        self.threads = []
        self.loopThread = threading.Thread(target=self.player.playloop)
        self.threads.append(self.loopThread)
        self.loopThread.start()
        """
        vlc360.sys.exit(self.app.exec_())

if __name__ == "__main__":
    logging.info("##osc_vlc started##")
    osc_serv = OscServer()
    logging.info("OscServer Initiated")
    osc_serv.start_osc()
    # osc_serv.start_server()

    servThread = vt.v_thread(target=osc_serv.start_server)
    servThread.start()
    logging.info("OscServer is listening")
    osc_serv.startVlc()
    servThread.stop()
