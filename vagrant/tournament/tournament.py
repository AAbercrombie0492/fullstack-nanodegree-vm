#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")
    


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    query = "delete from matches;"
    c.execute(query)
    db.commit()

    query2 = "update Players as p set Games_Played = m.match_count, Score = w.Win_Count from public.Player_Match_Count as m, public.Player_Win_Count as w where p.P_ID = m.P_ID and p.P_ID = w.P_ID;"
    c.execute(query2)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    query = "delete from players;"
    c.execute(query)
    db.commit()
    db.close()



def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    query = "select count(*) from players;"
    c.execute(query)
    rows = c.fetchall()
    count = int(str(rows[0][0]))
    db.close()
    return count


def registerPlayer(name):
    bleach.clean(name)
    db = connect()
    c = db.cursor()
    query = "insert into Players(Name, Games_Played, Score) VALUES(%s,0,0 );"
    c.execute(query, (name,))
    db.commit()
    db.close()

    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """


def playerStandings():
    db = connect()
    c = db.cursor()
    query = "select p_id, name, score, games_played from players order by score;" 
    c.execute(query)
    rows = c.fetchall()
    db.close()
    return rows

    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    bleach.clean(winner)
    bleach.clean(loser)
    db = connect()
    c = db.cursor()
    query = "insert into Matches(Round, P1, P2, Winner) Values(1,%d, %d, %d);" % (winner, loser, winner) 
    c.execute(query)
    db.commit()

    query2 = "update Players as p set Games_Played = m.match_count, Score = w.Win_Count from public.Player_Match_Count as m, public.Player_Win_Count as w where p.P_ID = m.P_ID and p.P_ID = w.P_ID;"
    c.execute(query2)
    db.commit()

    db.close()
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
def swissPairings():
    db = connect()
    c = db.cursor()
    query = "select P_ID, Name, Score from players;"
    c.execute(query)
    rows = c.fetchall()
    wincounts =sorted(rows, key=lambda tup: tup[2], reverse = True)

    from itertools import groupby
    groups = [list(g) for k,g in groupby(wincounts, lambda x: x[2])]

    pairs = [(i[j][0], i[j][1], i[j+1][0], i[j+1][1]) for i in groups for j in range(0,len(i),2)]

    return pairs



    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


