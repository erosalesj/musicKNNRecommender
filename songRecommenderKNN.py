import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from rapidfuzz import process
import json, smtplib, ssl, logging
from flask import Flask, request, jsonify
from time import sleep
import logging


#from dotenv import load_dotenv

# Load and clean Spotify one million songs dataset
df = pd.read_csv('spotify_one_million_song_dataset.csv')

# Remove rows with missing values
df_cleaned = df.dropna()

# Extract features of interest for recommendations
df_features = df_cleaned[['artist_name', 'track_name', 'genre', 'popularity', 'tempo', 'danceability', 'energy']].copy()


'''
user_item_matrix = user_ratings_df.pivot(
    index=["movieId"], columns=["userId"], values="rating"
).fillna(0)
'''

''''
# Define a KNN modle on consine similarity
cf_knn_model = NearestNeighbors(
    metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)


def song_recommender_engine(track_name, matrix, cf_model, n_recs):
    # Fit the model
    cf_knn_model = cf_model.fit(matrix)
    
    # Find the movie
    match = process.extractOne(track_name, movie_metadata['track_name'])
    if match[1] >= 80:  # Only accept matches with 80% or higher similarity
        movie_id = match[2]
        
        # Add this check
        if movie_id not in matrix.index:
            return f"Movie ID {movie_id} not found in ratings matrix"
            
        # Get recommendations
        distances, indices = cf_knn_model.kneighbors(
            matrix.loc[movie_id, :].values.reshape(1, -1), 
            n_neighbors=n_recs
        )
        # ... rest of the function

    else:
        return "No close movie match found. Please try a different movie title."

    # Add this debugging code before the kneighbors call
    print(f"Movie ID found: {movie_id}")
    print(f"Available indices: {matrix.index.tolist()[:5]}...")  # Show first 5 indices

    # Rest of the function remains unchanged
    distances, indices = cf_knn_model.kneighbors(matrix.loc[movie_id, :].values.reshape(1, -1), n_neighbors=n_recs)
    movie_rec_ids = sorted(
        list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
        key=lambda x: x[1],
    )[:0:-1]

    # List to store recommendations
    cf_recs = []
    for i in movie_rec_ids:
        cf_recs.append({"Title": movie_metadata["title"][i[0]], "Distance": i[1]})

    # Select top number of recommendations needed
    df = pd.DataFrame(cf_recs, index=range(1, n_recs))

    return df

'''


# KNN recommendation function
def knn_artist_recommendation(artist_name, k=5):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_features['genre'])

    #print(tfidf_matrix.head())
    print(tfidf_matrix.dtype)

    knn = NearestNeighbors(n_neighbors=k+1, metric='cosine')
    knn.fit(tfidf_matrix)

    idx = df_features[df_features['artist_name'].str.contains(artist_name, case=False, regex=False)].index
    if len(idx) == 0:
        print(f"No artist name containing '{artist_name}' found.")
        return []

    idx = idx[0]
    distances, indices = knn.kneighbors(tfidf_matrix[idx],n_neighbors=k+1)

    recommended_artists = df_features.iloc[indices[0]].artist_name.values[1:]
    return recommended_artists


print(knn_artist_recommendation("daft punk"))


# KNN recommendation function
def knn_artist_recommendation(track_name, k=5):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_features['genre'])

    knn = NearestNeighbors(n_neighbors=k+1, metric='cosine')
    knn.fit(tfidf_matrix)

    idx = df_features[df_features['track_name'].str.contains(track_name, case=False, regex=False)].index
    if len(idx) == 0:
        print(f"No track name containing '{track_name}' found.")
        return []

    idx = idx[0]
    distances, indices = knn.kneighbors(tfidf_matrix[idx],n_neighbors=k+1)

    recommended_titles = df_features.iloc[indices[0]].track_name.values[1:]
    return recommended_titles

#print(knn_recommendation("Around The World"))