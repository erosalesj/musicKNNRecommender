"""
ZeroMQ Server
"""
import time
import zmq
import json
import songRecommenderKNN
import genreQuery




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
    elif received_data["type"] == "recommend_by_genre":
        genre = received_data["genre"]
        print(f"Genre of interest is {genre}")
        # Process recommendation
        connection = genreQuery.createConnection()
        #cursor = genreQuery.createCursor()
        genreQuery.returnByGenre(connection, genre)
        
        rows = genreQuery.returnByGenre(connection, genre)
        
        recommendations = genreQuery.formartDict(connection, rows) 
    
        
    #print(f"The recommendations are {recommendations}")
    # recommendations_json = json.dumps(recommendations)
    socket.send_json(recommendations)

context.destroy()

"""
Song Genres:
acoustic
afrobeat
alt-rock
ambient
black-metal
blues
breakbeat
cantopop
chicago-house
chill
sqlite> select distinct genre from songs;
acoustic
afrobeat
alt-rock
ambient
black-metal
blues
breakbeat
cantopop
chicago-house
chill
classical
club
comedy
country
dance
dancehall
death-metal
deep-house
detroit-techno
disco
drum-and-bass
dub
dubstep
edm
electro
electronic
emo
folk
forro
french
funk
garage
german
gospel
goth
grindcore
groove
guitar
hard-rock
hardcore
hardstyle
heavy-metal
hip-hop
house
indian
indie-pop
industrial
jazz
k-pop
metal
metalcore
minimal-techno
new-age
opera
party
piano
pop
pop-film
power-pop
progressive-house
psych-rock
punk
punk-rock
rock
rock-n-roll
romance
sad
salsa
samba
sertanejo
show-tunes
singer-songwriter
ska
sleep
songwriter
soul
spanish
swedish
tango
techno
trance
trip-hopd
"""