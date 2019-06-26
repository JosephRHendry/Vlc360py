# Vlc360py

VLC Player Built on top of an OSC server with a focus on 360 video/ image

## installation ##
pip3 install python-vlc<br>
pip3 install python-osc

## Usage  ##
python3 osc_vlc.py<br>
simple_client.py

## OSC Commands ##
format: "/filter" [message]
A string indicating the function to run and a message consisting of a list of parameters

/vlc/file {filename}  #optional# [yaw, pitch, roll, fov]<br>
/vlc/pause<br>
/vlc/brightness {float 0-2.0}<br>
/vlc/fade {float level 0-2.0}<br>
etc. 

