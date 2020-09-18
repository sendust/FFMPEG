# ZMQ client for ffmpeg dynamic filter
# Made by sendust 2020/9/16
# Usage : zmqsends.py "tcp://localhost:5555" "hue s 2"
# This code contains .........
#  - socket timeout
#  - send test command
#  - Script timeout
#



import zmq
import sys
import threading
from multiprocessing import Process
from urllib.parse import urlparse

def url_validate(url):
    parts = urlparse(url)
    return all([parts.scheme, parts.netloc])

def script_timeout():
    print("Terminating current script......")
    raise SystemExit


if len(sys.argv) < 3:
    print("Usage......\r\n (example)\r\n zmqsends \"tcp://localhost:5555\" \"hue@filter1 s 0\"\r\n\r\n Sending test command.... \r\n " )
    address = "tcp://localhost:5555"
    text_to_send = "hue@filter1 s 0"
else:
    address = sys.argv[1]
    text_to_send = sys.argv[2]
    if not(url_validate(address)):
        print("Invalid address")
        exit(1)


threading.Timer(3, script_timeout).start

context = zmq.Context()


print("Connecting to server with address " , address)
socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.LINGER, 0)
socket.RCVTIMEO = 2000 # timeout in milisecont
socket.connect(address)


print("Sending request [", text_to_send, "]...")
socket.send_string(text_to_send)
try:
    print("Wait zmq replay ........")
    message = socket.recv()
    print("Received reply [", message, "]")

except zmq.ZMQError as e:
    print("ZMQ communication error .......")
    if e.errno == zmq.EAGAIN:
        pass  # no message was ready (yet!)
    else:
        traceback.print_exc()

print("Distroy zmq.......")
socket.close()
context.term()
