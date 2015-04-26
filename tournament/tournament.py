#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def connect_db(func):
    """decorator to streamline db connection related code"""
    def connect_db_and_call(*args, **kwargs):
        db = connect()
        c = db.cursor()
        kwargs['c'] = c
        result = func(*args, **kwargs)
        c.close()
        db.commit()
        db.close()
        return result
    return connect_db_and_call


@connect_db
def deleteMatches(c=None):
    """Remove all the match records from the database."""
    c.execute("delete from matches")


@connect_db
def deletePlayers(c=None):
    """Remove all the player records from the database."""
    c.execute("delete from players")


@connect_db
def countPlayers(c=None):
    """Returns the number of players currently registered."""
    c.execute("select count(*) from players")
    row = c.fetchone()
    return int(row[0])


@connect_db
def registerPlayer(name, c=None):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    c.execute("insert into players (name) values (%s);", (name,))


@connect_db
def playerStandings(c=None):
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
    c.execute("""
        select
            id, name,
            COALESCE(wins, 0) as wins,
            COALESCE(wins, 0) + COALESCE(losses, 0) as matches
        from
            players
                left join winners on players.id = winners.winner
                left join losers on players.id = losers.loser
        order by
            wins desc;
    """)
    rows = c.fetchall()
    return rows


@connect_db
def reportMatch(winner, loser, c=None):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c.execute("insert into matches (winner, loser) values (%s, %s)", (winner, loser))


def swissPairings():
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
    standings = playerStandings()
    pairs = [(standings[x][0],
              standings[x][1],
              standings[x+1][0],
              standings[x+1][1]) for x in xrange(0, len(standings), 2)]
    return pairs
