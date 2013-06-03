#!/usr/bin/env python
import sys, os
import web

sys.path.append(os.path.dirname(__file__))

import db
import controller
import forms

web.config.debug = True
urls = (
	'/', 'index',
	'/get_round', 'get_round',
)

render = web.template.render('/var/www/templates', cache=False)

class index:
	def GET(self):
		web.header('Content-Type', 'text/html')
		return "Hello, world"
#	def GET(self,data):
#		web.header('Content-Type', 'text/xml')
#		return "Hello, world"
#		return render.response("19366451048", data)
	def POST(self):
		data = web.input()
		try:
			if data.Text:
				agent = 'plivo'
				res = controller.handle(data.From, data.Text.lower(), data.Type)
		except AttributeError:
			agent = 'twilio'
			res = controller.handle(data.From[1:], data.Body.lower())
			
		web.header('Content-Type', 'text/xml')
		if agent == 'plivo':
			return render.response(data.From, res)
		elif agent == 'twilio':
			return render.twilio(data.From, res)

class get_round:
	def GET(self):
		render = web.template.render('/var/www/templates', cache=False)
		theform = forms.get_round()
		web.header('Content-Type', 'text/html')
		return render.get_round(theform)
	def POST(self):
		data = web.input()
		web.header('Content-Type', 'text/html')
		return render.scorecard(controller.get_round(data.number, data.round))

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()

def is_test():
	if 'WEBPY_ENV' in os.environ:
		return os.environ['WEBPY_ENV'] == 'test'

if (not is_test()) and  __name__ == "__main__": app.run()
