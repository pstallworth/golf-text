#!/usr/bin/env python
import sys, os
import web
from urlparse import urlparse, parse_qsl

try:
    import mymodel
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    try:
        import mymodel
    finally:
        sys.path.remove(os.path.dirname(__file__))

web.config.debug = True
urls = (
	'/', 'index',
	'/create_player', 'create_player',
	'/add_score', 'add_score',
	'/create_round', 'create_round',
	'/join_round', 'join_round',
	'/get_score', 'get_score',
)

class index:
	def GET(self):
		return "Hello, world, from web.py!"

class create_player:
	def POST(self):
		data = web.input()
		response = mymodel.create_player(data.number)
		return response

class create_round:
	def POST(self):
		data = web.input()
		response = mymodel.create_round(data.number)
		return response
class add_score:
	def POST(self):
		data = web.input()
		print "number=%s and score=%s" % (data.number,data.score)
		response = mymodel.add_score(data.number,data.score,2)		
		return response

class join_round:
	def POST(self):
		data = web.input()
		response = mymodel.join_round(data.number, data.round_id)
		return response

class get_score:
	def GET(self):
		data = web.input()
		response = mymodel.get_score(data.number, data.round_id)
		return response

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()	

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
