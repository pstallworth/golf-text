#!/usr/bin/env python
import web
# Should db connection go somewhere else?
db = web.database(dbn="mysql", db="golf", user="ubuntu", pw="ubuntu")

"""
 combine - returns the net score of the current round of the two players 
 whose names are are passed into the function.  If one of the two player's 
 names does not exist in the database, function exits.

 Because the query ORs the existence of the players we checked for both
 in the beginning, but this does mean that if one player doesn't finish the
 round, their partial scores can be used in calculating the net.
"""
def combine(player1, player2):

	if not check_player_name(player1):
		return "Player name %s not found" % player1
	elif not check_player_name(player2):
		return "Player name %s not found" % player2

	result = db.query("select hole, min(score) as score from scores inner join players "
					"on players.number = scores.number where "
					"players.current_round = scores.round_id "
					"AND (players.name = $player1 or players.name = $player2) "
					"group by hole", vars={'player1':player1,'player2':player2})

	if not result:
		return "query failed to return results"

	total_score = 0
	for res in result:
		total_score = total_score + res.score

	return "net %s" % total_score

def create_player(phone_number, name="golfer"):

	players = db.select("players",vars=locals(), what="number", where="number=$phone_number")

	if not players:
		# Player not found so add to database
		db.insert("players",number=phone_number, name=name)
		return "added player"
	else:
		# Player found, do not add
		return "player already exists"

def create_round(number):

# Create_round makes the assumption that if a player wanted to create
# a round then they wanted to be in that round as well, so the call to 
# join_round() at the end reflects that assumption

	rounds = db.select("rounds",what="round_id")
	rid = len(rounds)+1
	db.insert("rounds", number=number, round_id=rid, score=0, current_hole=1)
	join_round(number,rid)
	return rid

def join_round(number, round_id):

	if not check_player(number):
		# Number not in db, cannot join round, don't assume and don't add them yet
		return "invalid number to join_round()"
	elif not valid_round(round_id):
		return "invalid round id"
	else:
		result = db.where("rounds",number=number,round_id=round_id)
		if not result:
			db.insert("rounds",number=number,round_id=round_id,score=0, current_hole=1)

		db.update("players",where="number=$number",vars=locals(),current_round=round_id)
		return "joined round"

def add_score_new(number,new_score,hole=0):

	result = db.query("SELECT players.current_round,rounds.number,"
                    "current_hole,score FROM rounds INNER JOIN players ON "
                    "rounds.number = players.number AND "
                    "current_round = round_id AND "
                    "players.number = $number", vars={'number':number})

	if not result:
		return "Database error"
	
	for results in result:
		current_hole = results.current_hole
		rid = int(results.current_round)
		current_score = results.score

	if current_hole is None: 
		#BAIL
		return 'cannot continue scoring this round'

	db.insert("scores",number=number,round_id=rid,hole=current_hole,score=new_score)
	current_hole = current_hole + 1

	if current_hole < 19:
		db.query("UPDATE rounds SET score=$new_score+$current_score, "
				"current_hole=$current_hole WHERE round_id=$rid AND number=$number", 
				vars={'rid':rid,'new_score':new_score,'current_score':current_score,
				'number':number, 'current_hole':current_hole})
#		db.update("rounds",where="round_id=$rid and number=$number",vars=locals(),
#				score=new_score+current_score,current_hole=current_hole)
	else:
		db.update("rounds",where="round_id=$rid and number=$number",vars=locals(),
				current_hole=web.db.SQLLiteral('NULL'),score=current_score+new_score)

def add_score(number,score,hole=2):

# Deprecated
# now we are going to start tracking the hole the player is on

	if int(hole) < 1 or int(hole) > 18:
		print "invalid hole"
	elif int(score) < 1 or int(score) > 10:
		print "invalid score %s" % score
	elif not check_player(number):
		print "invalid number %s" % number
	else:
		result = db.select("players",what="current_round",vars=locals(),where="number=$number")
		if not result:
			#bad round id, dn't have current round
			print "no current round"
			return "failure"
		else:
			rid = result[0].current_round
			result = db.where("rounds",what="score",number=number,round_id=rid)
			current_score = result[0].score		
			db.update("rounds",where="number=$number",vars=locals(),round_id=rid,score=int(current_score)+int(score))
			return "success"

def get_score(number,round_id=0):
	# Input validation is first, success is last
	if not check_player(number):
		# Number doesn't exist in database, don't make assumption and create, simply notify
		return "number not found"
	elif round_id == 0:
		# Then they didn't pass in round id, return current round
		result = db.where("players",what="current_round",number=number)
		rid = int(result[0].current_round)
		result = db.where("rounds",what="score",round_id=rid,number=number)
		score = result[0].score
		print "score %s" % score
		return score
	else:
		# Round_id passed in, so use it
		result = db.where("rounds",what="score",round_id=round_id,number=number)
		if not result:
			print "invalid round id, maybe needs to be converted to int?"
			return "invalid round id"
		else:
			score = result[0].score
			print "score %s" % score
			return score

def check_player(number):
	result = db.where("players",number=number)
	if not result:
		return False
	elif result[0].number == number:
		return True

def check_player_name(name):
	result = db.where("players",name=name)

	if not result:
		return False
	elif result[0].name == name:
		return True

def valid_round(round_id):

	if round_id < 0:
		return False

	result = db.where("rounds",round_id=round_id)

	if not result: 
		return False
	else:
		return True;

def add_name(number, name):

	db.update("players",where="number=$number",vars=locals(),name=name)

