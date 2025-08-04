import sqlite3

def createConnection():
    ''' Create a game datase if not already created '''
    connection = sqlite3.connect('songsData.db')
    return connection

def closeConnection(connection):
    connection.close()


def createCursor(connection):
    cursor = connection.cursor
    return cursor


def returnByGenre(connection, genre, table="songs"):
    cur = connection.cursor()
    cur.execute(f"""
    SELECT * FROM {table}
    WHERE genre = ?
    ORDER BY popularity DESC
    LIMIT 10;
    """, (genre,))
    result = cur.fetchall()
    result_arr = list(result)
    return result_arr

def formartDict(connection, arr):
    result = []
    for row in arr:
        record = {
            "title": row[0],
            "artist_name": row[1],
            "genre": row[3],
            "popularity": row[2]}
        result.append(record)
    results = {"recommendations": result}

    return results

    """
    for track, artist, genre, pop in zip(all_recommended_track_name, all_recommended_artist, all_recommended_genre, all_recommended_popularity):
        rec = {
            "title": track,
            "artist": artist,
            "genre": genre,
            "popularity": int(pop)
            }
        all_recommendations["recommendations"].append(rec)
    """
    #return all_recommendations

def returnAll(connection, table):
    cur = connection.cursor()
    cur.execute(f'SELECT * FROM {table};')
    result = cur.fetchall()
    return result




