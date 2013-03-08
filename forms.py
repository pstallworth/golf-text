import web
from web import form

get_round = form.Form(
	form.Textbox("number"),
	form.Textbox("round"))
