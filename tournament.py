#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# store the most recently selected tournament
current_tournament = 0
current_connection = 0

def initTournament(tournament):
    """Reset data from the specified tournament"""
    ctx = getContext(tournament)
    deleteMatches(ctx["tournament"])
    deletePlayers(ctx["tournament"])

def getContext(tournament, title=False):
    """Return a dictionary with either a specifically selected tournament or the most recent entered
    into the system alongside the DB connection object
    """
    global current_tournament
    global current_connection
    if not current_connection:
        current_connection =  connect()

    ctx = {
        "db": current_connection,
        "tournament": tournament
    }
    if not ctx["tournament"]:
        if current_tournament:
            ctx["tournament"] = current_tournament

        else:
            if title:
                cursor = ctx["db"].cursor()
                cursor.execute("SELECT t_id FROM tournament WHERE title = %s", (title,))
                ctx["db"].commit()
                row = cursor.fetchone()
                if row:
                    current_tournament = row[0]

            else:
                cursor = ctx["db"].cursor()
                cursor.execute("SELECT MAX(t_id) AS recent_t_id FROM tournament")
                ctx["db"].commit()
                row = cursor.fetchone()
                if row:
                    current_tournament = row[0]


            if not current_tournament:
                cursor.execute("INSERT INTO tournament (title) VALUES (%s) RETURNING t_id",(title,))
                ctx["db"].commit()
                row = cursor.fetchone()
                if row:
                    current_tournament = row[0]

            ctx["tournament"] = current_tournament

    return ctx


def execQueryAndCommit(query, tournament, parms=None, return_all=False):
    ctx = getContext(tournament)
    cursor = ctx["db"].cursor()
    cursor.execute(query, parms)
    ctx["db"].commit()
    try:
        data = cursor.fetchall()
        if not return_all:
            return data[0][0]

        else:
            return data

    except psycopg2.ProgrammingError:
        return

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def deleteMatches(tournament = False):
    """Remove all the match records from the database."""

    execQueryAndCommit(
        r"DELETE FROM match USING match_player WHERE match.t_id = %s AND match.m_id = match_player.m_id",
        **{
            "parms": (tournament,),
            "tournament": tournament
        }
    )

def deletePlayers(tournament = False):
    """Remove all the player records from the database."""

    execQueryAndCommit(
        r"DELETE FROM player WHERE t_id = %s",
        **{
            "parms": (tournament,),
            "tournament": tournament
        }
    )

def countPlayers(tournament = False):
    """Returns the number of players currently registered."""

    return execQueryAndCommit(
        "SELECT COUNT(*) FROM player WHERE t_id = %s",
        **{
            "parms": (tournament,),
            "tournament": tournament
        }
    )

def registerPlayer(name, tournament = False):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    return execQueryAndCommit(
        "INSERT INTO player (t_id, name) VALUES (%s,%s) RETURNING p_id",
        **{
            "parms": (tournament, name),
            "tournament": tournament
        }
    )

def playerStandings(tournament = False):
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

    data = execQueryAndCommit(
        "SELECT * FROM standings WHERE t_id = %s",
        **{
            "parms": (tournament,),
            "tournament": tournament,
            "return_all": True
        }
    )
    return [ ( row[0], row[1], row[2], row[3] ) for row in data ]


def reportMatch(winner, loser, tournament = False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    current_match = execQueryAndCommit(
        "INSERT INTO match (t_id, winner) VALUES (%s,%s) RETURNING m_id",
        **{
            "parms": (tournament, winner),
            "tournament": tournament
        }
    )

    execQueryAndCommit(
        "INSERT INTO match_player (m_id, p_id, win) VALUES (%s,%s,1)",
        **{
            "parms": (current_match, winner),
            "tournament": tournament
        }
    )

    execQueryAndCommit(
        "INSERT INTO match_player (m_id, p_id, win) VALUES (%s,%s,0)",
        **{
            "parms": (current_match, loser),
            "tournament": tournament
        }
    )

def swissPairings(tournament = False):
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

    ctx = getContext(tournament)
    standings = playerStandings(ctx["tournament"])

    pairs = []
    while standings:
        pair = standings[:2]
        standings = standings[2:]
        pairs.append((pair[0][0], pair[0][1], pair[1][0], pair[1][1]))

    return pairs




