"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import vlc360_qt_5 as vlc360
import threading
import time

from pythonosc import dispatcher
from pythonosc import osc_server

class OSC_Server(vlc360.Player):
  def start_osc(self): #__init__(self):
    self.parser = argparse.ArgumentParser()
    self.parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    self.parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")
    self.args = self.parser.parse_args()

    self.dispatcher = dispatcher.Dispatcher()
    self.messages = []

  def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))

  def print_compute_handler(unused_addr, args, volume):
    try:
      print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError: pass

  def add_message(unused_addr, args, volume):
    print("args :", args)
    print("volume :", volume)

  def pause(self, word, word2, word3):
    if(self.player.mediaplayer.get_state() == vlc360.vlc.State.Playing):
      print("Howdy")
      self.player.mediaplayer.pause()
    else:
      self.player.mediaplayer.pause()
      print("FAIL :", self.player.mediaplayer.get_state())
      print("State :" ,self.player.mediaplayer.get_state() == vlc360.vlc.State.Paused)
    #print(self.player.mediaplayer.get_state())

  def report_back(unused_addr, args, volume):
    if self.messages == True: return self.messages
    else: return False

  def start_server(self):
    self.dispatcher.map("/filter", print)
    self.dispatcher.map("/pause", self.pause, "Hi")

    self.dispatcher.map("/volume", self.print_volume_handler, "Volume")
    self.dispatcher.map("/logvolume", self.print_compute_handler, "Log volume", math.log)

    self.server = osc_server.ThreadingOSCUDPServer(
        (self.args.ip, self.args.port), self.dispatcher)
    print("Serving on {}".format(self.server.server_address))
    self.server.serve_forever()

  def startVlc(self):

      self.player = vlc360.Player()
      self.player.show()
      self.player.showFullScreen()

      # player.resize(640, 480)
      self.player.resize(1024, 768)
      if vlc360.sys.argv[1:]:
          self.player.OpenFile(vlc360.sys.argv[1])

      self.threads = []
      # playThread = threading.Thread(target = player.mediaplayer.play)
      self.player.mediaplayer.play()

      exit_flag = threading.Event()

      self.loopThread = threading.Thread(target=self.player.playloop)

      self.threads.append(self.loopThread)
      self.loopThread.start()

      """
      Test of loading time
      for x in range(5):
        time.sleep(5)
        self.player.mediaplayer.set_mrl('V2.mp4')
        self.player.mediaplayer.play()
      """
      vlc360.sys.exit(self.app.exec_())


if __name__ == "__main__":
    osc_serv = OSC_Server()
    osc_serv.start_osc()
    servThread = threading.Thread(target=osc_serv.start_server)
    servThread.start()
    osc_serv.startVlc()

