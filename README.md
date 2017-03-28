# FSND P3 - Tournament Results

Relational SQL Database and implementing outline functionality

## Installation

This module uses a database backend based on PostgreSQL relying on the `psycopg2` module, wich can be obtained using

	pip install psycopg2

To install the database, please use the ```tournament.sql``` file hosted with this repository.
The installation goes like this.

**BEWARE: the installation drops any database by the name of `tournament`. Please make sure You
have no such database under this name in place. All data will be lost!**

	prompt: psql
	----------------------------------------------
	psql (9.3.16)
	Type "help" for help.

	vagrant=> \i path/to/tournament.sql

## Usage

The module supports multiple tournaments. If you wish for a 

	# Import the module
	from tournament import *

	#
	# 1) If you wish to set a specific tournament you may set it up
	# expility at the start
	my_tournament = getContext(False, "My Tournament")["tournament"]

	#
	# 2) Make sure you clean the tournament data before you start entering fresh data
	initTournament(my_tournament)

	#
	# 3) Insert players. Make it an even number.
	registerPlayer("Example player1", my_tournament):
	registerPlayer("Example player2", my_tournament):

	#
	# 4) Get your first pairings
	pairings = swissPairings(my_tournament)

	#
	# 5) Report matches by settin the parameters to the reportMatch function to the
	# id of the winner followed by the loser.
	reportMatch(id_winner, id_loser, my_tournament)

	#
	# 6) Read the current standings as a list of tuples. The first one wins!
	standings = playerStandings(my_tournament)


## Files included

* `tournament.py (md5: 0746e7ca9de31f7acc0db7a1db0d5164)`
* `tournament.sql (md5: 8f285eb4250b7466caf262f0ae4eed29)`
* `tournament_test.py (md5: 7f67161e1a890c968dd78cf6f0b68e0d)`
* `README.md-template (md5: 14d1a265f3ba8020487b256bd4af0297)`

## Version

2017-03-28T22:40:08.048000