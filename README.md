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

* `tournament.py (md5: 800fee6b0da20dfc323f64b9600d7e3c)`
* `tournament.sql (md5: b1517bc363c6c21210630c7f76e3e032)`
* `tournament_test.py (md5: 3cbee77924d9fa6623fe9ac68b8fe9f8)`
* `tournament_test_multi_tournaments.py (md5: a7c31d99530832fdb570eca8823e3689)`
* `README.md-template (md5: 3846df3b2ecc707ef0ff36e523b4587e)`

## Version

2017-03-28T22:44:03.966000