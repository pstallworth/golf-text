#!/usr/bin/env python
import web
# Should db connection go somewhere else?
#db = web.database(dbn="mysql", db="golf", user="root", pw="passw0rd")
db = web.database(dbn="mysql", db="golf", user="ubuntu", pw="ubuntu")


def create_player(phone_number):

	players = db.select("players",vars=locals(), what="number", where="number=$phone_number")

	if not players:
		# Player not found so add to database
		db.insert("players",number=phone_number)
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
	db.insert("rounds", number=number, round_id=rid, score=0)
	join_round(number,rid)
	return rid

def join_round(number, round_id):

	if not check_player(number):
		# Number not in db, cannot join round, don't assume and add them yet
		return "invalid number to join_round()"
	elif not valid_round(round_id):
		return "invalid round id"
	else:
		result = db.where("rounds",number=number,round_id=round_id)
		if not result:
			db.insert("rounds",number=number,round_id=round_id,score=0)

		db.update("players",where="number=$number",vars=locals(),current_round=round_id)
		return "joined round"

def add_score(number,score,hole=2):

#we are disregarding the hole at this point so you can simply send your score

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
		return False;
	elif result[0].number == number:
		return True;

def valid_round(round_id):

	if round_id < 0:
		return False

	result = db.where("rounds",round_id=round_id)

	if not result: 
		return False
	else:
		return True;
