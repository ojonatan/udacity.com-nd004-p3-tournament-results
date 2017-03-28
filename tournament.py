#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# store the most recently selected tournament
current_tournament = 0
current_connection = 0

def get_context(tournament):
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
            cursor = ctx["db"].cursor()
            cursor.execute("SELECT MAX(t_id) AS recent_t_id FROM tournament")
            ctx["db"].commit()
            current_tournament = cursor.fetchone()[0]
            if not current_tournament:
                cursor.execute("INSERT INTO tournament (title) VALUES ('default') RETURNING t_id")
                ctx["db"].commit()
                current_tournament = cursor.fetchone()[0]

    return ctx

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def deleteMatches(tournament = False):
    """Remove all the match records from the database."""

    ctx = get_context(tournament)
    cursor = ctx["db"].cursor()
    cursor.execute("DELETE FROM match USING match_player WHERE match.t_id = %s AND match.m_id = match_player.m_id", (current_tournament,))
    ctx["db"].commit()

def deletePlayers(tournament = False):
    """Remove all the player records from the database."""

    ctx = get_context(tournament)
    cursor = ctx["db"].cursor()
    cursor.execute("DELETE FROM player WHERE t_id = %s", (current_tournament,))
    ctx["db"].commit()

def countPlayers(tournament = False):
    """Returns the number of players currently registered."""

    ctx = get_context(tournament)
    cursor = ctx["db"].cursor()
    cursor.execute("SELECT COUNT(*) FROM player WHERE t_id = %s", (current_tournament,))
    return cursor.fetchone()[0]

def registerPlayer(name, tournament = False):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    ctx = get_context(tournament)
    cursor = ctx["db"].cursor()
    cursor.execute("INSERT INTO player (t_id, name) VALUES (%s,%s) RETURNING p_id", (current_tournament,name))
    current_player = cursor.fetchone()[0]
    ctx["db"].commit()

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

    ctx = get_context(tournament)
    cursor = ctx["db"].cursor()
    query = """
        SELECT
            P.p_id AS id,
            P.name,
            COUNT(W.win) AS wins,
            COUNT(M.m_id) AS matches

        FROM
            player AS P

        LEFT JOIN
            match AS X ON(
                X.t_id = P.t_id
            )

        LEFT JOIN
            match_player AS M ON(
                M.p_id = P.p_id AND
                M.m_id = X.m_id
            )

        LEFT JOIN
            match_player AS W ON(
                W.m_id = X.m_id AND
                W.p_id = P.p_id AND
                W.win = 1
            )

        WHERE
            P.t_id = %s

        GROUP BY
            P.p_id

        ORDER BY
            wins DESC

    """

    cursor.execute(
        query,
        (current_tournament,)
    )
    return [ ( row[0], row[1], row[2], row[3] ) for row in cursor.fetchall() ]


def reportMatch(winner, loser, tournament = False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    ctx = get_context(tournament)
    cursor = ctx["db"].cursor()
    cursor.execute("INSERT INTO match (t_id, winner) VALUES (%s,%s) RETURNING m_id", (current_tournament,winner))
    current_match = cursor.fetchone()[0]
    cursor.execute("INSERT INTO match_player (m_id, p_id, win) VALUES (%s,%s,1)", (current_match,winner))
    cursor.execute("INSERT INTO match_player (m_id, p_id, win) VALUES (%s,%s,0)", (current_match,loser))
    ctx["db"].commit()

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
    ctx = get_context(tournament)

    standings = playerStandings(ctx["tournament"])

    pairs = []
    while standings:
        pair = standings[:2]
        standings = standings[2:]
        pairs.append((pair[0][0], pair[0][1], pair[1][0], pair[1][1]))

    return pairs




