import webapp2
import jinja2
import os

from google.appengine.ext import db

"""
The program is a basic blog
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

class Blog(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(Handler):

	def get(self):
		visits = self.request.cookies.get('visits', '0')
		if visits.isdigit():
			visits = int(visits) + 1
		else:
			visits = 0
		self.response.headers.add_header('Set-Cookie', 'visits = %s' % visits)
		blogs = db.GqlQuery("select * from Blog order by created desc")
		self.render("Blog_Front.html", blogs = blogs, db = db, n = visits)

	def post(self):
		blogs = db.GqlQuery("select * from Blog order by created desc")
		self.render("Blog_Front.html", blogs = blogs)

class FormHandler(Handler):

	def get(self):
		self.render("Blog_Form.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			blog = Blog(subject = subject , content = content)
			blog.put()
			self.redirect("/blog/permalink")
		else:
			self.response.out.write("Error : Please fill in all fields")

class PermaHandler(Handler):

	def get(self):
		blogs = db.GqlQuery("select * from Blog order by created desc limit 1")
		blog = blogs.get()
		self.render("Blog_Perma.html", blog = blog)

	def post(self):
		blogs = db.GqlQuery("select * from Blog order by created desc limit 1")
		blog = blogs.get()
		self.render("Blog_Perma.html", blog = blog)
		
app = webapp2.WSGIApplication([
	('/blog', MainHandler),
	('/blog/newpost', FormHandler),
	('/blog/permalink', PermaHandler)
	])