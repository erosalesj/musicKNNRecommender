"""
ZeroMQ Client Demo
"""

import zmq
import json

context = zmq.Context()

print("Connecting to server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

request_payload_1 = {
    "type": "recommend_by_genre",
    "genre": "rock"
}

request_payload_2 = {
    "type": "recommend_by_artist",
    "artist": "kylie minogue"
}

request_payload_3 = {
    "type": "recommend_by_track",
    "track": "Crimewave"
}


socket.send_json(request_payload_1)  # genre
#socket.send_json(request_payload_2) # artist 
#socket.send_json(request_payload_3) # track

message = socket.recv()
print(f"Received reply {message}")
