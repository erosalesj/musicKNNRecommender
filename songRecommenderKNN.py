import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
#from rapidfuzz import process
import json, smtplib, ssl, logging
#from flask import Flask, request, jsonify
from time import sleep
import logging
import pickle
# Replace Dask imports with joblib
from joblib import Parallel, delayed, dump, load

#from dotenv import load_dotenv

# Load and clean Spotify one million songs dataset
df = pd.read_csv('spotify_one_million_song_dataset.csv')

# Remove rows with missing values
df_cleaned = df.dropna()

# Extract features of interest for recommendations
df_features = df_cleaned[
    ['artist_name',
    'track_name',
    'genre',
    'popularity',
    'tempo',
    'danceability',
    'energy']].copy()


def knn_artist_recommendation_pickle(k=5, n_jobs=-1):
    """ Create KNN model and save model with Joblib locally"""
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_features['genre'])
    knn = NearestNeighbors(n_neighbors=k+1, metric='cosine', n_jobs=n_jobs)
    knn.fit(tfidf_matrix)
    dump(knn, 'knn_artist_recommendation_model.joblib')


def knn_artist_recommendation_from_model(artist_name, model_path="knn_artist_recommendation_model", k=5):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_features['genre'])

    # load model from disk using joblib
    loaded_model = load(model_path)
    idx = df_features[df_features['artist_name'].str.contains(artist_name, case=False, regex=False)].index
    if len(idx) == 0:
        print(f"No artist name containing '{artist_name}' found.")
        return []

    idx = idx[0]
    distances, indices = loaded_model.kneighbors(tfidf_matrix[idx].reshape(1, -1), n_neighbors=k+1)

    recommendations_df = df_features.iloc[indices[0]][['artist_name', 'track_name', 'genre', 'popularity']].iloc[1:]
    all_recommended_track_name = recommendations_df['track_name'].values
    all_recommended_artist = recommendations_df['artist_name'].values
    all_recommended_genre = recommendations_df['genre'].values
    all_recommended_popularity = recommendations_df['popularity'].values

    all_recommendations = {"recommendations": []}

    for track, artist, genre, pop in zip(all_recommended_track_name, all_recommended_artist, all_recommended_genre, all_recommended_popularity):
        rec = {
            "title": track,
            "artist": artist,
            "genre": genre,
            "popularity": int(pop)
            }
        all_recommendations["recommendations"].append(rec)

    return all_recommendations


#print(knn_artist_recommendation_from_model("Crystal Castles"))


# KNN recommendation function
def knn_artist_recommendation(artist_name, k=5, n_jobs=-1):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_features['genre'])
    knn = NearestNeighbors(n_neighbors=k+1, metric='cosine', n_jobs=n_jobs) # Use n_jobs parameter for parallelization
    knn.fit(tfidf_matrix)

    idx = df_features[df_features['artist_name'].str.contains(artist_name, case=False, regex=False)].index
    if len(idx) == 0:
        print(f"No artist name containing '{artist_name}' found.")
        return []

    idx = idx[0]
    distances, indices = knn.kneighbors(tfidf_matrix[idx].reshape(1, -1), n_neighbors=k+1)

    recommendations_df = df_features.iloc[indices[0]][['artist_name', 'track_name', 'genre', 'popularity']].iloc[1:]
    all_recommended_track_name = recommendations_df['track_name'].values
    all_recommended_artist = recommendations_df['artist_name'].values
    all_recommended_genre = recommendations_df['genre'].values
    all_recommended_popularity = recommendations_df['popularity'].values

    all_recommendations = {"recommendations": []}

    for track, artist, genre, pop in zip(all_recommended_track_name, all_recommended_artist, all_recommended_genre, all_recommended_popularity):
        rec = {
            "title": track,
            "artist": artist,
            "genre": genre,
            "popularity": int(pop)
            }
        all_recommendations["recommendations"].append(rec)

    return all_recommendations

#print(knn_artist_recommendation("crystal castles"))


def knn_track_recommendation(track_name, k=5, n_jobs=-1):
    """
    Recommend tracks similar to the provided track name using KNN with parallelization
    
    Parameters:
    -----------
    track_name : str
        Name of the track to find similar tracks for
    k : int
        Number of recommendations to return. Default 5
    n_jobs : int
        Number of parallel jobs to run (-1 means using all processors)
    """
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_features['genre'])

    knn = NearestNeighbors(n_neighbors=k+1, metric='cosine', n_jobs=n_jobs)    # Use n_jobs parameter for parallelization
    knn.fit(tfidf_matrix)

    idx = df_features[df_features['track_name'].str.contains(track_name, case=False, regex=False)].index
    if len(idx) == 0:
        print(f"No track name containing '{track_name}' found.")
        return []

    idx = idx[0]
    distances, indices = knn.kneighbors(tfidf_matrix[idx].reshape(1, -1), n_neighbors=k+1)

    recommendations_df = df_features.iloc[indices[0]][['artist_name', 'track_name', 'genre', 'popularity']].iloc[1:]
    all_recommended_track_name = recommendations_df['track_name'].values
    all_recommended_artist = recommendations_df['artist_name'].values
    all_recommended_genre = recommendations_df['genre'].values
    all_recommended_popularity = recommendations_df['popularity'].values

    all_recommendations = {"recommendations": []}

    for track, artist, genre, pop in zip(all_recommended_track_name, all_recommended_artist, all_recommended_genre, all_recommended_popularity):
        rec = {
            "title": track,
            "artist": artist,
            "genre": genre,
            "popularity": int(pop)
            }
        all_recommendations["recommendations"].append(rec)

    return all_recommendations

#print(knn_track_recommendation("Crimewave"))