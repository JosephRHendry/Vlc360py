"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import vlc360_qt_7 as vlc360
import threading
import time

from pythonosc import dispatcher
from pythonosc import osc_server

class OSC_Server(vlc360.Player):
  def start_osc(self): #__init__(self):
    self.parser = argparse.ArgumentParser()
    #self.parser.add_argument("--ip",
    #                    default="127.0.0.1", help="The ip to listen on")
    self.parser.add_argument("--ip",
                             default="192.168.248.137", help="The ip to listen on")
    self.parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")
    self.args = self.parser.parse_args()

    self.dispatcher = dispatcher.Dispatcher()
    self.messages = []
    self.threads = []

  def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))

  def print_compute_handler(unused_addr, args, volume):
    try:
      print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError: pass

  def add_message(unused_addr, args, volume):
    print("args :", args)
    print("volume :", volume)

  """def load_file(self, args, file):
      print("Hi", args[0], file)
      i = vlc360.vlc.Instance()
      m = i.media_new(str(file))
      print(m)
      m.get_mrl()
      self.player.mediaplayer.set_media(m)
      self.player.mediaplayer.play()"""
  def load_file(self, args, file, coords= [0, 0, 0, 0]):
      i = vlc360.vlc.Instance()
      m = i.media_new(str(file))

      yaw = coords[0]
      pitch = coords[1]
      roll = coords[2]
      field_of_view = coords[3]
      v = vlc360.vlc.VideoViewpoint(yaw, pitch, roll, field_of_view)
      print(file, coords, v)

      print(m)
      m.get_mrl()

      #self.player.mediaplayer.video_update_viewpoint(v, True)

      self.player.mediaplayer.set_media(m)
      self.player.mediaplayer.play()
      vlc360.vlc.libvlc_video_update_viewpoint(self.player.mediaplayer, v, True)

  def pan(self, args, coords=[0,0,0,0]):
      """
      Continuously pans around in all directions at the increments specified
      :param args: list
      :param coords: pitch, yaw roll
      :return:
      """
      print("pan_cont")

      yaw = coords[0]
      pitch = coords[1]
      roll = coords[2]
      field_of_view = coords[3]
      v = vlc360.vlc.VideoViewpoint(yaw, pitch, roll, field_of_view)
      #print("v :", v)
      self.player.mediaplayer.v = v

      if len(self.threads) == 0:
          self.loopThread = threading.Thread(target=self.player.playloop(v))
          self.threads.append(self.loopThread)
          self.loopThread.start()

      #else:
      #    self.player.mediaplayer.video_update_viewpoint(v, False)


  def pov(self, args, coords=[0, 0, 0, 0]):
     """
     Sets a playing video to the specified coordinates
     :param args: a list
     :param coords: here the first element of the list will be coords, ie a list of 4 variables, yaw, pitch, roll, fov
     :return:
     """
      print("pov")
      yaw = coords[0]
      pitch = coords[1]
      roll = coords[2]
      field_of_view = coords[3]
      v = vlc360.vlc.VideoViewpoint(yaw, pitch, roll, field_of_view)
      print("v :",v)
      self.player.mediaplayer.video_update_viewpoint(v, True)

  def play(self, file, args):
      """
      Deprecated - see load_file, an overloaded version of the same function
      :param file:
      :param args:
      :return:
      """
      i = vlc360.vlc.Instance()
      m = i.media_new('V1.mp4')
      m.get_mrl()
      self.player.mediaplayer.set_media(m)
      self.player.mediaplayer.play()

  def pause(self, word, word2, word3):
    if(self.player.mediaplayer.get_state() == vlc360.vlc.State.Playing):
      self.player.mediaplayer.pause()
    #else:
      #self.player.mediaplayer.pause()
    #print(self.player.mediaplayer.get_state())

  def report_back(unused_addr, args, volume):
    if self.messages == True: return self.messages
    else: return False

  def start_server(self):
    self.dispatcher.map("/filter", print)
    self.dispatcher.map("/pause", self.pause, "Hi")

    self.dispatcher.map("/volume", self.print_volume_handler, "Volume")
    self.dispatcher.map("/logvolume", self.print_compute_handler, "Log volume", math.log)
    self.dispatcher.map("/vlc/file", self.load_file)
    self.dispatcher.map("/vlc/pov", self.pov)
    self.dispatcher.map("/vlc/pan", self.pan)

    self.server = osc_server.ThreadingOSCUDPServer(
        (self.args.ip, self.args.port), self.dispatcher)
    print("Serving on {}".format(self.server.server_address))
    self.server.serve_forever()

  def startVlc(self):
      #coords = [40, 20, 140, 80]
      #file = 'V1.mp4'

      self.instance = vlc360.vlc.Instance()

      #self.m = self.instance.media_new(file)

      self.player = vlc360.Player()
      self.player.show()
      # self.player.showFullScreen()


      #print(file, coords, v)

      #print(self.m)
      #self.m.get_mrl()

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
    osc_serv = OSC_Server()
    osc_serv.start_osc()
    servThread = threading.Thread(target=osc_serv.start_server)
    servThread.start()
    osc_serv.startVlc()

