import cgi
import re
import webapp2
import itertools


USER_RE_EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
USER_RE_PASSWORD = re.compile(r"^.{3,20}$") 
USER_RE_USERNAME = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

form = """
<html>
	<head>
		<title> Sign Up </title>
	</head>

	<body >
		<h1> Signup </h1>
		<form method = "post" action = "/welcome">
			<table >
				<tr>
					<td align = "right">
						<label> Username <input type = "text" name = "username"> </label> <br><br>
					</td>
					<td style = "color : red ;  padding-bottom :15px ;"  >%(username_error)s</td>
				</tr>
				<tr>
					<td align = "right">
						<label> Password <input type = "password" name = "password"> </label> <br><br>
					<td style = "color : red ;  padding-bottom :15px ;" >%(password_error)s</td>
					</td>
				</tr>
				<tr>
					<td align = "right">
						<label> Verify Password <input type = "password" name = "verify"> </label><br> <br>
					</td>
					<td style = "color : red ;  padding-bottom :15px ;" >%(verify_password_error)s</td>
				</tr>
				<tr>
					<td align = "right">
						<label> Email(optional) <input type = "text" name = "email"> </label> <br><br>
					</td>
					<td style = "color : red ;  padding-bottom :15px ;">%(email_error)s</td>
				</tr>
			</table>	
			<input type = "submit">
		</form>
	</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):

	def get(self):
		#form = form %  {'username_error' : '', 'password_error' : '', 'email_error' : '' } 
		username_error = self.request.get('username_error')
		password_error = self.request.get('password_error')
		email_error = self.request.get('email_error')
		verify_password_error = self.request.get('verify_password_error')
		a = { 'username_error' : username_error, 'password_error' : password_error, 
		'email_error' : email_error, 'verify_password_error' : verify_password_error }
		self.response.write(form %  (a))

		

class WelcomeHandler(webapp2.RequestHandler):

	def get(self):
		self.response.write("This is the get website");

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		redirect_string = "/signup"
		list_function_outputs = self.get_list()
		true_count = 0;
		'''		
		for i in list_function_outputs :
			if list_function_outputs[i] == True:
				list_function_outputs += 1


		if(list_function_outputs > 1):
			and_string = "&"
		else:
			and_string = ""
		'''	
		first_flag = 0
		welcome_flag = True

		if(self.valid_username(username) == None):
			welcome_flag = False
			if first_flag == 0:
				redirect_string += "?" + "username_error=Invalid"
				first_flag = 1
		
		if(self.valid_password(password) == None):
			welcome_flag = False
			if first_flag == 0:
				redirect_string += "?" + "password_error=Invalid"
				first_flag = 1
			else:
				redirect_string += "&password_error=Invalid"

		if(self.valid_email(email) == None):
			welcome_flag = False
			if first_flag == 0:
				redirect_string += "?" + "email_error=Invalid"
				first_flag = 1
			else:
				redirect_string += "&email_error=Invalid"

		if(self.valid_password_match(password, verify) == False):
			welcome_flag = False
			if first_flag == 0:
				redirect_string += "?" + "verify_password_error=Invalid"
				first_flag = 1
			else:
				redirect_string += "&verify_password_error=Invalid"


		print "redirect_string = " + str(redirect_string)
		print "welcome_flag =  " + str(welcome_flag)
		print self.valid_username(username)
		if welcome_flag:
			self.response.write("Welcome dear " + username)
		else:
			self.redirect(redirect_string)

		
			
	def get_list(self):
		return [ self.valid_username, self.valid_password, self.valid_email, self.valid_password_match ]


	def valid_username(self, username):
		return USER_RE_USERNAME.match(username)

	def valid_password(self, password):
		return USER_RE_PASSWORD.match(password)

	def valid_email(self, email):
		return USER_RE_EMAIL.match(email)

	def valid_password_match(self, password_1, password_2):
		if password_1 == password_2:
			return True
		else:
			return False


app = webapp2.WSGIApplication([
	('/signup', MainHandler),
	('/welcome', WelcomeHandler)
	],
	debug = True)
