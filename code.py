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
)

class index:
	def GET(self):
		return "Hello, world, from web.py!"

class create_player:
	def POST(self):
		return "Adding player... " 

	def GET(self):
		return "Getting players..."

class create_round:
	def POST(self):
		return "<h1>Recorded " + user_data.score + " on hole " + user_data.hole + "</h1>"
	

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()	

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
