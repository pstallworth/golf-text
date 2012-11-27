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
	else:
		return "invalid command"
