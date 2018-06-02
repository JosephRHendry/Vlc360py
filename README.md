# Vlc360py

VLC Player Built on top of an OSC server with a focus on 360 video/ image

## installation ##
pip3 install python-vlc<br>
pip3 install python-osc

## Usage  ##
python3 osc_vlc_360.py<br>
osc_simple_client.py

## OSC Commands ##
/vlc/file {filename}  #optional# [yaw, pitch, roll, fov]<br>
/vlc/pause
/vlc/brightness {float 0-2.0}
/vlc/fade {float level 0-2.0}
etc. 

