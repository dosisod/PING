from ezws import EZWS
import smtplib
import json
import os

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
		self.ez=EZWS(config, ua, output=False) #makes new EZWS obj

		try: #opens each file and saves it
			with open(pwdf) as f:
				self.pwd=f.read()

			with open(usrf) as f:
				self.usr=f.read()

			with open(mailf) as f:
				self.mail=f.read()

		except FileNotFoundError:
			raise ValueError("files storing username, password, or gmail are non-existent")

		if os.path.exists(last):
			with open(last, "w+") as f:
				self.last=json.load(f)
		else:
			self.last=[]

	def grab(self): #EZWS grabs info
		self.ez.grab()
		self.data=self.ez.data

	def unique(self): #gets new data points and creates msg
		new=[]
		for i in self.data:
			if i not in self.last:
				new.append(i)
		
		self.data=new

	def send(self): #sends gmail
		smtps=smtp.SMTP_SSL("smtp.gmail.com",465)
		smtps.ehlo()
		smtps.login(self.usr, self.pwd)
		smtps.sendmail(self.usr, self.mail, self.msg)

	def auto(self): #grabs and closes automatically
		self.grab()
		print(self.data)
		#print(self.data)
		#self.send()
