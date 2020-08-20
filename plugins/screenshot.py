import mss

class Screenshot(object):
	def __init__(self):
		self.ss_object = ""

	def take_ss(self):
		"""
		"""
		with mss.mss() as sc:
			for num, monitor in enumerate(sc.monitors[1:], 1):
				self.ss_object = sc.grab(monitor)

	def dump(self):
		self.take_ss()
		return self.ss_object