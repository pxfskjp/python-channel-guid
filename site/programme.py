import datetime

class Programme:
	def __init__(self):
		self.name = "Test Program"
		self.start = datetime.datetime.now()
		self.duration = datetime.timedelta(hours=1)