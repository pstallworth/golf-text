#!/usr/bin/env python
import web
db = web.database(dbn="mysql", db="golf", user="root", pw="passw0rd")

def create_player(phone_number):
	players = db.select("players",vars=locals(), what="number", where="number=$phone_number")

	if not players:
		#player not found so add to database
		db.insert("players",number=phone_number)
		print "player added..."
	else:
		#player found, do not add
		print "player not found"

def create_round(phone_number):
	rounds = db.select("rounds",what="round_id")
	rid = len(rounds)+1
	db.insert("rounds", number=phone_number, round_id=rid, score=0)
	join_round(phone_number,rid)
	
def join_round(phone_number, round_id):
	db.update("players",where="number=$phone_number",vars=locals(),current_round=round_id)

def add_score(number,hole,score):
	if (hole < 1 or hole > 18):
		#invalid hole
		print "invalid hole"
	elif (score < 1 or score > 10):
		#invalid score
		print "invalid score"
	else:
		result = db.select("players",what="current_round",vars=locals(),where="number=$number")
		rid = result[0].current_round
		result = db.where("rounds",what="score",number=number,round_id=rid)
		current_score = result[0].score		
		db.update("rounds",where="number=$number",vars=locals(),round_id=rid,score=current_score+score)

def get_score(number,round_id=0):
	if (round_id == 0):
		#then they didn't pass in round id, return current round
		result = db.where("players",what="current_round",number=number)
		rid = int(result[0].current_round)
		result = db.where("rounds",what="score",round_id=rid,number=number)
		score = result[0].score
		print "current score is:",score
	else:
		#round_id passed in, so use it
		result = db.where("rounds",what="score",round_id=round_id,number=number)
		score = result[0].score
		print "current score of passed in round:", score

