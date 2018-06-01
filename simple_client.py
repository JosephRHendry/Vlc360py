"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--ip", default="127.0.0.1",
    #    help="The ip of the OSC server")
    parser.add_argument("--ip", default="192.168.248.137",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    for x in range(1):
        client.send_message("/filter", random.random())
        file = "V2.mp4"
        coords = [20, 0, 0, 80]
        message = [file, coords]
        # client.send_message("/pause", True)
        # client.send_message("/vlc/file", file)
        client.send_message("/vlc/file", message)
        time.sleep(1)
        coords = [0.04, 0.0, 0.00, 0.0]
        message = [coords]

        time.sleep(1)
        # client.send_message("/vlc/pov", message)
        # time.sleep(1)
        client.send_message("/vlc/pan", message)
        time.sleep(1)
        coords = [0, 0, 0, 0]
        message = [coords]
        # client.send_message("/vlc/pan", message)
        #yaw = 200
        #message = [yaw]
        #client.send_message("/vlc/yaw", message)



        level = -2.0
        message=[level]
        #client.send_message("/vlc/fade", message)
        time.sleep(2)


        #level = 1
        #message=[level]
        #client.send_message("/vlc/fade", message)

