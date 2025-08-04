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
    SELECT *
    FROM(
        SELECT *
        FROM {table}
        WHERE genre = ?
        ORDER BY popularity DESC
        LIMIT 200
        )
    ORDER BY RANDOM()
    LIMIT 10;    
        """, (genre,))
    result = cur.fetchall()
    result_arr = list(result)
    return result_arr


def formartDict(connection, arr):
    result = []
    for row in arr:
        record = {
            "title": row[1],
            "artist_name": row[0],
            "genre": row[3],
            "popularity": row[2]}
        result.append(record)
    results = {"recommendations": result}

    return results


def returnAll(connection, table):
    cur = connection.cursor()
    cur.execute(f'SELECT * FROM {table};')
    result = cur.fetchall()
    return result
