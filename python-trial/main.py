import os
import webapp2
import jinja2

from google.appengine.ext import db

"""
Program demonstrates user sign in using cookies
"""

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainHandler(Handler):

	def get(self):
		self.render("4_login.html")

	def post(self):
		username = str(self.request.get('username'))
		self.response.headers.add_header('Set-Cookie', 'username = monkey; Path = /)')
		self.redirect("/welcome")

class WelcomeHandler(Handler):

	def get(self):
		username = self.request.cookies.get('username')
		self.render("4_welcome.html", username = username)

app = webapp2.WSGIApplication([
	('/signup', MainHandler),
	('/welcome', WelcomeHandler)
	])