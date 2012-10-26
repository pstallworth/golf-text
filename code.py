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

try:
	import controller
except ImportError:
	sys.path.append(os.path.dirname(__file__))
	try:
		import controller
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

render = web.template.render('/var/www/templates', cache=False)

class index:
	def GET(self):
		web.header('Content-Type', 'text/xml')
		return render.response("Hello Index Page")
	def POST(self):
		data = web.input()
		res = controller.handle(data.From, data.Text, data.Type)
		web.header('Content-Type', 'text/xml')
		return render.response(data.From, res)

class create_player:
	def POST(self):
		data = web.input()
		res = mymodel.create_player(data.number)
		return render.response(res)

class create_round:
	def POST(self):
		data = web.input()
		res = mymodel.create_round(data.number)
		return render.response(res)
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

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
