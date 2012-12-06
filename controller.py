#!/usr/bin/env python
try:
    import mymodel
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    try:
        import mymodel
    finally:
        sys.path.remove(os.path.dirname(__file__))


def handle(number, message, mtype):
	
	cmd_str = message.split()
	
	if cmd_str[0] == "create":
		mymodel.create_player(number)
		return "player created" 
	elif cmd_str[0] == "round":
		round_id = mymodel.create_round(number)
		return "round id %s" % round_id
	elif cmd_str[0] == "join" and len(cmd_str) == 2:
		return mymodel.join_round(number, cmd_str[1])
	elif cmd_str[0] == "score" and len(cmd_str) == 2:
		return mymodel.add_score_new(number,int(cmd_str[1]))
	elif cmd_str[0] == "score" and len(cmd_str) == 1:
		return mymodel.get_score(number)
	elif cmd_str[0] == "name" and len(cmd_str) == 2:
		return mymodel.add_name(number, cmd_str[1])
	elif cmd_str[0] == 'combine' and len(cmd_str) == 3:
		return mymodel.combine(cmd_str[1], cmd_str[2])
	elif cmd_str[0] == 'compare' and len(cmd_str) == 3:
		return mymodel.compare(cmd_str[1], cmd_str[2])
	elif cmd_str[0] == 'match' and len(cmd_str) == 5:
		return mymodel.match(cmd_str[1], cmd_str[2], cmd_str[3], cmd_str[4])
	else:
		return "invalid command"
