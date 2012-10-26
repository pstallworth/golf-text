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

	if cmd_str[0] == "round":
		round_id = mymodel.create_round(number)
		return "round id %s" % round_id

	try:
		if cmd_str[0] == "join":
			return mymodel.join_round(number, cmd_str[1])
	except IndexError:
		return "invalid or no round given to join"

	try:	
		if cmd_str[0] == "score" and cmd_str[1] is not None:
			mymodel.add_score(number,cmd_str[1])
			return "score added"
	except IndexError:
		return mymodel.get_score(number)

	return "invalid command"
