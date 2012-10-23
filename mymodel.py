#!/usr/bin/env python
import web
# Should db connection go somewhere else?
db = web.database(dbn="mysql", db="golf", user="root", pw="passw0rd")


def create_player(phone_number):
	players = db.select("players",vars=locals(), what="number", where="number=$phone_number")

	if not players:
		# Player not found so add to database
		db.insert("players",number=phone_number)
		print "player added..."
	else:
		# Player found, do not add
		print "player not found"


def create_round(number):
""" Create a new round

	create_round makes the assumption that if a player wanted to create
	a round then they wanted to be in that round as well, so the call to 
	join_round() at the end reflects that assumption

"""
	rounds = db.select("rounds",what="round_id")
	rid = len(rounds)+1
	db.insert("rounds", number=number, round_id=rid, score=0)
	join_round(number,rid)


def join_round(number, round_id):

	if not check_player(number):
		# Number not in db, cannot join round, don't assume and add them yet
		print "invalid number to join_round()"
	elif not valid_round(round_id:)
	else:
		db.update("players",where="number=$number",vars=locals(),current_round=round_id)


def add_score(number,hole,score):
	if hole < 1 or hole > 18:
		print "invalid hole"
	elif score < 1 or score > 10:
		print "invalid score"
	elif not check_player(number):
		print "invalid number"
	else:
		result = db.select("players",what="current_round",vars=locals(),where="number=$number")
		rid = result[0].current_round
		result = db.where("rounds",what="score",number=number,round_id=rid)
		current_score = result[0].score		
		db.update("rounds",where="number=$number",vars=locals(),round_id=rid,score=current_score+score)


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
		print "current score is:",score
	else:
		# Round_id passed in, so use it
		result = db.where("rounds",what="score",round_id=round_id,number=number)
		# TODO what is result if round_id is bogus?
		score = result[0].score
		print "current score of passed in round:", score

def check_player(number):
	result = db.where("players",number=number)
	if not result: # TODO check this syntax in if clause, what is result here?
		return false;
	elif result[0].number == number:
		return true;

def valid_round(round_id):

	if round_id < 0:
		return false

	result = db.where("rounds",round_id=round_id)

	if not result: # TODO what is result here if 1 round in db...4 rounds?
		return false
	else:
		return true;
