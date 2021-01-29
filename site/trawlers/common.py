import abc
from abc import ABCMeta
import datetime

class Trawler:
	__metaclass__ = ABCMeta

	# Return JSON for the week's programmes
	@staticmethod
	def get_info_for_days(days):
		return "none"


def correct_timezone_offsets(schedule):
	for i,date in enumerate(schedule):
		sched = schedule[date]
		sched_day = datetime.datetime.strptime(date, "%Y-%m-%d")
		print sched_day
	pass