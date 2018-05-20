import sys
import vlc
import ctypes
from PyQt5 import QtGui, QtWidgets, QtCore
import threading

#import vlc_position

class Player(QtWidgets.QMainWindow):
    """A simple Media Player using VLC and Qt
        """

    def __init__(self, master=None):

        self.app = QtWidgets.QApplication(sys.argv)
        QtWidgets.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")
        self.exit_flag = threading.Event()

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = False
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":  # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_F:
            if self.switch == 0:
                self.showFullScreen()
                self.switch = 1
            else:
                self.showNormal()
                self.switch = 0
    def playloop(self, v):
        while not self.exit_flag.wait(timeout=0.01):
            self.mediaplayer.video_update_viewpoint(self.mediaplayer.v, False)
            continue


    def createUI(self):
        """ Set up the user interface, signals & slots
            """
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin":  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window,
                              QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.widget.setLayout(self.vboxlayout)


    def PlayPause(self):
        """Toggle play/pause status
            """


    def Stop(self):
        """Stop player
            """


    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
            """


    #    if filename is None:
    #        filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
    #        if not filename:
    #            return

    def setVolume(self, Volume):
        """Set the volume
            """


    def setPosition(self, position):
        """Set the position
            """


    # the vlc MediaPlayer needs a float value between 0 and 1, Qt
    # uses integer variables, so you need a factor; the higher the 
    # factor, the more precise are the results
    # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()




#if __name__ == "__main__":
#   p = Player()
#   p.startVlc()
