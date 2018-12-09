from email.mime.text import MIMEText
from ezws import EZWS
import smtplib
import json
import os

class PING:
	def __init__(self, ua, pwdf="pass", usrf="user", mailf="mail", lastf="last.json", config="config.json", string=False):
		"""
		ua     user agent to use for EZWS parser
		pwdf   password file for email
		usrf   username file for email
		mailf  filename of email to send the email
		lastf  json file stroing info on last scrape
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

		self.lastf=lastf
		if os.path.exists(lastf):
			with open(lastf, "r+") as f:
				self.last=json.load(f)
		else:
			self.last=[]

	def grab(self): #EZWS grabs info
		self.ez.grab()
		self.data=self.ez.data

	def unique(self): #gets new data points and creates msg
		new=[]
		for link in self.data:
			if link["url"] not in [i["url"] for i in self.last]:
				new.append(link) #appends all link data if link has never been seen
			else:
				indexid=[i["url"] for i in self.last].index(link["url"]) #get index of dict storing url of current link
				indextemp={"url":link["url"],"data":[]}
				for info in link["data"]:
					if info not in self.last[indexid]["data"]:
						indextemp["data"].append(info) #if there is new info in the site, add it temp
				if indextemp["data"]:
					new.append(indextemp) #if there was any new info in site add temp to new

		self.last=self.data
		self.newdata=new

	def body(self):
		self.msg=""
		if self.newdata:
			for site in self.newdata:
				self.msg+="Link "+site["url"]+" added:\n"
				for collection in site["data"]:
					for cell in collection:
						self.msg+=cell+" "
					self.msg+="\n"

	def send(self): #sends gmail
		if self.msg:
			mime=MIMEText(self.msg)
			smtps=smtplib.SMTP_SSL("smtp.gmail.com",465)
			smtps.login(self.usr, self.pwd)
			smtps.sendmail(self.usr, self.mail, mime.as_string())
		else:
			print("nothing new")

	def save(self):
		with open(self.lastf,"w+") as f:
			json.dump(self.last,f)

	def auto(self): #pre-built use case
		self.grab()
		self.unique()
		self.save()
		self.body()
		self.send()
