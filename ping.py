from ezws import EZWS
import smtplib

class PING:
	def __init__(self, ua, pwdf="pass", usrf="user", mailf="mail", last="last.json", config="config.json", string=False):
		"""
		ua     user agent to use for EZWS parser
		pwdf   password file for email
		usrf   username file for email
		mailf  filename of email to send the email
		last   json file stroing info on last scrape
		config EZWS formatted json file
		string set to true if passing string not filename
		"""

		try: #opens each file and saves it
			with open(pwdf) as f:
				self.pwd=f.read()

			with open(usr) as f:
				self.usr=f.read()

			with open(mailf) as f:
				self.mail=f.read()

			self.ez=EZWS(config, ua) #makes new EZWS obj
		except FileNotFoundError:
			raise ValueError("files storing username, password, or gmail are non-existent")
