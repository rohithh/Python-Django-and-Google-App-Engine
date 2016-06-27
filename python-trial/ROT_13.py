import webapp2
import cgi
import codecs

form =  """
<html>
<head>
	<title> The ROT-13 Page </title>
</head>
<body>
	<h1> Enter some text to ROT 13: </h1>


	<form method = "post" action = "/">
	<textarea name = "text" height = "50px" width = "100px">%(answer)s</textarea>

		<br>
		<input type = "submit">
	</form>
</body>
</html>
"""




class MainHandler(webapp2.RequestHandler):

	def write_answer(self, answer = ""):
		self.response.write(form % {'answer' : answer})

	def get(self):
		self.write_answer("")

	def post(self):
		result = self.request.get("text")
		result = self.rot_13(result)
		result = cgi.escape(result)
		self.write_answer(result)
		#self.redirect("/result")

	def rot_13(self, result):
		return codecs.encode(result, "rot_13")

class ResultHandler(webapp2.RequestHandler):

	def post(self):
		result = self.request.get("text")
		result = self.rot_13(result)
		result = cgi.escape(result)
		self.write_answer(result)

	def write_answer(self, answer = ""):
		self.response.write(form % {'answer' : answer})

	def rot_13(self, result):
		return codecs.encode(result, "rot_13")


app = webapp2.WSGIApplication([('/', MainHandler),
 ("/result", ResultHandler)], 
 debug = True)
