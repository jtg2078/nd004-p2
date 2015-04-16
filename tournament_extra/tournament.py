#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament_extra")


def deleteMatches(tournament=None):
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    if tournament:
        c.execute("delete from matches where tournament = %s", (tournament, ))
    else:
        c.execute("delete from matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players")
    db.commit()
    db.close()


def deleteTournamentPlayers(tournament=None):
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    if tournament:
        c.execute("delete from tournament_players where tournament = %s", (tournament, ))
    else:
        c.execute("delete from tournament_players")
    db.commit()
    db.close()


def deleteTournaments(tournament=None):
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    if tournament:
        c.execute("delete from tournaments where id = %s", (tournament, ))
    else:
        c.execute("delete from tournaments")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players")
    row = c.fetchone()
    db.close()
    return int(row[0])


def countTournamentPlayers(tournament=None):
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    if tournament:
        c.execute("select count(*) from tournament_players where tournament = %s", (tournament, ))
    else:
        c.execute("select count(*) from tournament_players")
    row = c.fetchone()
    db.close()
    return int(row[0])


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players (name) values (%s) RETURNING id;", (name,))
    db.commit()
    player_id = c.fetchone()[0]
    db.close()
    return int(player_id)


def registerTournament(name):
    """Adds a tournament to the tournament_extra database."""
    db = connect()
    c = db.cursor()
    c.execute("insert into tournaments (name) values (%s) RETURNING id;", (name,))
    db.commit()
    tournament_id = c.fetchone()[0]
    db.close()
    return int(tournament_id)


def registerTournamentPlayer(player, tournament):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into tournament_players (id, player, tournament) values (%s, %s, %s) RETURNING id;",
              ("{0}-{1}".format(tournament, player), player, tournament))
    db.commit()
    tournament_player_id = c.fetchone()[0]
    db.close()
    return tournament_player_id


def tournamentPlayerStandings(tournament):
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
    db = connect()
    c = db.cursor()
    c.execute("""
        select
            tournament_players.id,
            players.name,
            COALESCE(wins, 0) as wins,
            COALESCE(wins, 0) + COALESCE(losses, 0) as matches
        from
            tournament_players
            left join
                (
                    select
                        winner, count(winner) as wins
                    from
                        matches
                    where
                        tournament = %(tournament)s
                    group by
                        winner
                ) as winners
            on
                tournament_players.id = winners.winner
            left join
                (
                    select
                        loser, count(loser) as losses
                    from
                        matches
                    where
                        tournament = %(tournament)s
                    group by
                        loser
                ) as losers
            on
                tournament_players.id = losers.loser
            join
                players
            on
                tournament_players.player = players.id
        where
            tournament_players.tournament = %(tournament)s
        order by
            wins desc,
            tournament_players.id
    """, {'tournament': tournament})
    rows = c.fetchall()
    db.close()
    return rows


def reportMatch(tournament, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches (tournament, winner, loser) values (%s, %s, %s)", (tournament, winner, loser))
    db.commit()
    db.close()


def swissPairings(tournament):
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
    standings = tournamentPlayerStandings(tournament)
    pairs =  [(standings[x][0],
               standings[x][1],
               standings[x+1][0],
               standings[x+1][1]) for x in xrange(0, len(standings), 2)]
    return pairs
