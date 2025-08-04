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

    if received_data["type"] == "recommend_by_artist":
        artist = received_data["artist"]
        print(f"Artist of interest is {artist}")
        # Process recommendation
        recommendations = songRecommenderKNN.knn_artist_recommendation(artist)
    elif received_data["type"] == "recommend_by_track":
        track = received_data["track"]
        print(f"Track of interest is {track}")
        # Process recommendation
        recommendations = songRecommenderKNN.knn_track_recommendation(track)
        
    #print(f"The recommendations are {recommendations}")
    # recommendations_json = json.dumps(recommendations)
    socket.send_json(recommendations)

context.destroy()
