"""
ZeroMQ Client Demo
"""

import zmq
import json

context = zmq.Context()

print("Connecting to server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


'''
request_payload = {
    "type": "recommend_by_genre",
    "genre": "rock"
}

'''
'''
request_payload = {
    "type": "recommend_by_artist",
    "artist": "kylie minogue"
}

'''
request_payload = {
    "type": "recommend_by_track",
    "track": "Crimewave"
}


socket.send_json(request_payload)

message = socket.recv()
print(f"Received reply {message}")
