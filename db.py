#!/usr/bin/env python
import web
import os
# Should db connection go somewhere else?

def add_name(number, name):

	db.update("players",where="number=$number",vars=locals(),name=name)

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

"""
  deprecating
  back_nine - returns the score for the last 9 holes
"""
def back_nine(number):
	
	current_round = get_current_round(number)
	results = db.select("scores",vars=locals(),what="score",
					where="number=$number AND round_id=$current_round "
					"AND hole >= 10 AND hole < 19")

	if not results or results is None:
		return "No current round for player"

	currScore = 0
	for result in results:
		currScore += result.score

	return currScore

"""
  back_nine - returns sum of scores for last 9 holes
"""
def back_nine_new(number):

	current_round = get_current_round(number)
	results = db.select("scores", var=locals(), what="sum(score) as score",
				where="number=$number and round_id=$current_round "
				"AND hole >= 10 AND hole <= 18")

	if not results or results is None:
		return "No current round for player"

	return results[0].score

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


"""
  compare - compares the scores of the two players passed in and 
  returns the name of the winning player for the match. If one
  of the two players d.n.e in the database, function exits.
"""
def compare(player1, player2):

	if not check_player_name(player1):
		return "Player name %s not found" % player1
	elif not check_player_name(player2):
		return "Player name %s not found" % player2

	result = db.query("select sum(S.score) as player1, sum(T.score) as player2 from " 
				"scores S inner join scores T on S.hole = T.hole inner join players P "
				"on P.number = S.number inner join players R on R.number = T.number " 
				"where P.name = $player1 and R.name = $player2 ",
				vars={'player1':player1,'player2':player2})[0]

	if not result:
		return "Error, could not run scores"

	return result

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

	result = db.query("select sum(best_scores.scores) as low_score from "
					"(select hole, min(score) as score from scores inner join players "
					"on players.number = scores.number where "
					"players.current_round = scores.round_id "
					"AND (players.name = $player1 or players.name = $player2) "
					"group by hole) best_scores", vars={'player1':player1,'player2':player2})

	if not result:
		return "error: could not run scores"

	return "net %s" % result[0].low_score

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

	rid = db.insert("rounds", number=number, score=0, current_hole=1)
	return rid

"""
  deprecating
  front_nine - returns the scores for the first 9 holes
"""
def front_nine(number):

	current_round = get_current_round(number)
	results = db.select("scores",vars=locals(),what="score",
					where="number=$number AND round_id=$current_round " 
					"AND hole >= 1 AND hole < 10")

	if not results or results is None:
		return "No current round for the player"
	
	currScore = 0
	for result in results:
		currScore += result.score

	return currScore

"""
  front_nine - returns score for first 9 holes
"""
def front_nine_new(number):

	current_round = get_current_round(number)
	results = db.select("scores", var=locals(), what="sum(score) as score",
				where="number=$number and round_id=$current_round "
				"AND hole >= 1 AND hole <= 9")

	if not results or results is None:
		return "No current round for player"

	return results[0].score

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
		return result[0].score
	else:
		# Round_id passed in, so use it
		result = db.where("rounds",what="score",round_id=round_id,number=number)
		if not result:
			#print "invalid round id, maybe needs to be converted to int?"
			return "invalid round id"
		else:
			score = result[0].score
			#print "score %s" % score
			return score

def get_name(number):
	
	result = db.select("players", what="name", where="number=$number", vars=locals())
	return result[0].name

def get_current_round(number):
	
	results = db.select("players",what="current_round", where="number=$number",vars=locals())

	return results[0].current_round

"""
	gets the current hole from the current round
"""
def get_current_hole(number):

	curr_round = get_current_round(number)

	#at this point curr_round could be null
	if curr_round is None:
		return None

	res = db.select("rounds", what="current_hole", where="round_id=$curr_round", vars=locals())
	return res[0].current_hole


"""
   get_number_by_name
"""
def get_number_by_name(name):

	res = db.select("players",vars=locals(), what="number", where="name=$name") 

	return res[0].number

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

"""
   nassau - runs two player nassau
"""
def nassau(player1, player2):

	for player in (player1, player2):
		if not check_name(player):
			return "Player %s not found" % player

	p1number = get_number_by_name(player1)
	p2number = get_number_by_name(player2)

"""
	trying to refactor this to only do one thing, write new score
	calculations leading up to here having been moved out to controller.py
"""
def new_add_score(number, round_id, current_hole, hole_score, tot_score):

	db.insert("scores", number=number, round_id=round_id, hole=current_hole, score=hole_score)

	current_hole = current_hole + 1
	
	if current_hole < 19:
		db.query("UPDATE rounds SET score=$tot_score, current_hole=$current_hole "
				"WHERE round_id=$round_id AND number=$number", 
				vars={'round_id':round_id,'tot_score':tot_score, 'number':number, 
				'current_hole':current_hole})
	else:
		db.update("rounds",where="round_id=$rid and number=$number",vars=locals(),
				current_hole=web.db.SQLLiteral('NULL'),score=tot_score)

"""
  match - plays a 4-player, 2v2 match and returns the winning team
  Input assumption is that player1 and player2 are on the same team
  and player3 and player4 are on the same team.  The help for this function
  will show it used like match team1 team1 team2 team2 or something similar
  to indicate where the playeres for each team belong
"""
def match(player1, player2, player3, player4):

	for player in (player1, player2, player3, player4):
		if not check_player_name(player):
			return "Player %s not in system" % player

	
	team1 = combine(player1, player2).split()
	team2 = combine(player3, player4).split()

	if team1[1] < team2[1]:
		return "%s and %s win" % (player1, player2)
	elif team2[1] < team1[1]:
		return "%s and %s win" % (player3, player4)
	else:
		return "Tie"
	
"""
  scores - returns list of all submitted scores for current round
"""
def scores(number, round_id=0):
	
	if round_id == 0:
		current_round = get_current_round(number)
		results = db.select("scores",vars=locals(), what="hole,score", where="number=$number and round_id=$current_round")
	else:
		results = db.select("scores",vars=locals(), what="hole,score", where="number=$number and round_id=$round_id")

	if not results or results is None:
		return "No current round for player"

	#send this back to phone
	if round_id == 0:
		scoresString = ""
		for result in results:
			scoresString = scoresString + "%s:%s, " % (result.hole,result.score)
	else:
	#send this back to browser
		return results
	
	return scoresString 

def valid_round(round_id):

	if round_id < 0:
		return False

	result = db.where("rounds",round_id=round_id)

	if not result: 
		return False
	else:
		return True;


