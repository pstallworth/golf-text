#!/usr/bin/env python
try:
    import db
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    try:
        import db
    finally:
        sys.path.remove(os.path.dirname(__file__))


def handle(number, message, mtype):
	
	cmd_str = message.split()
	
	if cmd_str[0] == "create":
		return db.create_player(number)
	elif cmd_str[0] == "round":
		round_id = db.create_round(number)
		db.join_round(number, round_id)
		return "round id %s" % round_id
	elif cmd_str[0] == "join" and len(cmd_str) == 2:
		return db.join_round(number, cmd_str[1])
	elif cmd_str[0] == "score" and len(cmd_str) == 2:
		# need the round id, current hole, and total score to send to the new
		# score command
		return db.new_add_score(number, db.get_current_round(number),
					db.get_current_hole(number), cmd_str[1], int(db.get_score(number)) + int(cmd_str[1]))

		#return db.add_score_new(number,int(cmd_str[1]))
	elif cmd_str[0] == "score" and len(cmd_str) == 1:
		return db.get_score(number)
	elif cmd_str[0] == "name" and len(cmd_str) == 2:
		return db.add_name(number, cmd_str[1])
	elif cmd_str[0] == "name" and len(cmd_str) == 1:
		return db.get_name(number)
	elif cmd_str[0] == 'combine' and len(cmd_str) == 3:
		return db.combine(cmd_str[1], cmd_str[2])
	elif cmd_str[0] == 'compare' and len(cmd_str) == 3:
		res = db.compare(cmd_str[1], cmd_str[2])
		if res.player1 < res.player2:
			return "%s wins by %s" % (cmd_str[1], abs(res.player1 - res.player2))
		elif res.player2 < res.player1:
			return "%s wins by %s" % (cmd_str[2], abs(res.player2 - res.player1))
		else:
			return "Tie"
	elif cmd_str[0] == 'match' and len(cmd_str) == 5:
		return db.match(cmd_str[1], cmd_str[2], cmd_str[3], cmd_str[4])
	elif cmd_str[0] == 'scores' and len(cmd_str) == 1:
		return db.scores(number)
	elif cmd_str[0] == 'front' and len(cmd_str) == 1:
		return db.front_nine(number)
	elif cmd_str[0] == 'back' and len(cmd_str) == 1:
		return db.back_nine(number)
	else:
		return "invalid command"
