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


def tournamentPlayerStandings(tournament, with_bye=False):
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
            tournament_players.wins,
            tournament_players.matches
            {extra}
        from
            tournament_players
            join
                players
            on
                tournament_players.player = players.id
        where
            tournament_players.tournament = %(tournament)s
        order by
            wins desc,
            opponent_match_wins(tournament_players.id) desc,
            tournament_players.id
    """.format(extra=', tournament_players.had_bye' if with_bye else ''), {'tournament': tournament})
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
    c.execute("update tournament_players set wins = wins + 1, matches = matches + 1 where id = %s", (winner, ))
    c.execute("update tournament_players set matches = matches + 1 where id = %s", (loser, ))
    db.commit()
    db.close()


def reportTiedMatch(tournament, p1, p2):
    """Records the outcome of a single match between two players.

    Args:
      p1:  the id number of the player 1
      p2:  the id number of the player 2
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches (tournament, p1, p2) values (%s, %s, %s)", (tournament, p1, p2))
    c.execute("update tournament_players set matches = matches + 1 where id = %s", (p1, ))
    c.execute("update tournament_players set matches = matches + 1 where id = %s", (p2, ))
    db.commit()
    db.close()


def reportByeMatch(tournament, winner):
    """Records the outcome of a bye match.

    Args:
      winner:  the id number of the player who won
    """
    db = connect()
    c = db.cursor()
    c.execute("""update tournament_players
                 set wins = wins + 1, matches = matches + 1, had_bye = TRUE
                 where id = %s""", (winner, ))
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
    standings = tournamentPlayerStandings(tournament, with_bye=True)
    if len(standings) % 2 != 0:
        """
        with odd number of players, the following rule is used to find player for bye match
            1. iterate through the standing from top to bottom
            2. for each player
                - if player's had_bye is FALSE
                    - assign this player to have bye match for this round
                - else
                    - continue to next player
        """
        player_found = False
        for i in range(len(standings)):
            had_bye = standings[i][4]
            if had_bye is False:
                standings.insert(i+1, ('bye', 'bye', 0, 0))
                player_found = True
                break
        if player_found is False:
            raise ValueError("Unable to setup bye match, every players already had bye match")
    pairs =  [(standings[x][0],
               standings[x][1],
               standings[x+1][0],
               standings[x+1][1]) for x in xrange(0, len(standings), 2)]
    return pairs
