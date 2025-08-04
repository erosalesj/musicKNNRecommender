"""
ZeroMQ Client Demo
"""

import zmq
import json

context = zmq.Context()

print("Connecting to server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#data = {"artist": "kylie Minogue"}
data = {"artist": "daft punk"}
socket.send_json(data)

message = socket.recv()
print(f"Received reply {message}")
