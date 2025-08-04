"""
ZeroMQ Server
"""
import time
import zmq
import json
import songRecommenderKNN


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    received_data = socket.recv_json()
    print(f"Received request: {received_data}")

    # parse artist
    artist = received_data["artist"]
    print(f"Artist of interest is {artist}")

    # Process recommendatio
    recommendations = songRecommenderKNN.knn_artist_recommendation(artist)
    print(f"The recommended artist are {recommendations}")

    # Do some work
    # time.sleep(1)
    recommendations_json = json.dumps(recommendations)
    socket.send_json(recommendations)

context.destroy()