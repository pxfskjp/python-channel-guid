
from .common import Trawler

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import json
import datetime
from datetime import date, time


def total_secs(delta):
	return (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10**6) / 10**6


URL="http://www.subhavaarthatv.com/program.php"

def group(lst, n):
	for i in range(0, len(lst), n):
		val = lst[i:i+n]
		if len(val) == n:
			yield tuple(val)

def get_subha_day(date, day_number):
	# if day_name == "monday":
	# 	return []
	# print date
	response = urllib2.urlopen(URL)
	output = response.read()
	soup = BeautifulSoup(output)
	# print soup
	# print day_name
	div = soup.findAll("div", attrs={"id": "tabcontent"+str(day_number)})[0]
	# print div
	g = list(group(div.findAll("div"), 2))
	

	# return	# print table

	days_programs = []

	# midday_reached = false
	# will_reach_midday = false
	pm_hit = False
	noon = False
	for row in g:
		times_txt = row[0].text#.replace("noon", "pm")
		noon_temp = ("noon" in times_txt)

		if ("am" in times_txt) and pm_hit:
			continue



		times = times_txt.split("-")
		starts = times[0].strip()

		ptime = datetime.datetime.combine(date, datetime.datetime.strptime( starts.replace(":", ".")  ,  "%H.%M"    ).time())
		pm = noon and (ptime.time().hour < 12)
		if pm:
			pm_hit = True


		if pm:
			ptime += datetime.timedelta(hours=12)

		# if ptime.hour < 12:
		# 	continue

		# ptime -= datetime.timedelta(hours=12, minutes=30)
		# print ptime

		if noon_temp:
			noon = True

		link = row[1].text
		# print link


		days_programs.append({ "date": date.strftime("%Y-%m-%d"), "starts": ptime.strftime("%H%M"), "starts_datetime": ptime, "program_name": link })



	length = len(days_programs)
	for index, prog in enumerate(days_programs):
		if index == length - 1:
			next_prog = {"starts_datetime": datetime.datetime.combine(date + datetime.timedelta(days=1), datetime.datetime.min.time()) }
		else:
			next_prog = days_programs[index+1]

		if prog["program_name"] == "prev":
			prog["program_name"] = days_programs[index-1]["program_name"]

		duration = next_prog["starts_datetime"] - prog["starts_datetime"]
		durmins = int(total_secs(duration)/60)
		# print "this: " + str(prog["starts_datetime"]) + ", next: " + str(next_prog["starts_datetime"])
		# print durmins
		days_programs[index]["duration"] = durmins

	for prog in days_programs:
		del prog["starts_datetime"]


	return days_programs


BY_DAYS = [2,3,4,5,6,7,1]

def get_subha_week():
	schedule = {}

	today = datetime.date.today()
	days_since_monday = today.weekday()
	monday = today - datetime.timedelta(days=days_since_monday)
	for i in range(0, 7):
		date = monday + datetime.timedelta(days=i)
		schedule[date.strftime("%Y-%m-%d")] = get_subha_day(date, BY_DAYS[i])
	
	# print schedule
	return schedule


# print get_subha_day(datetime.date.today(), "5")

class TrawlerSubha(Trawler):
	@staticmethod
	def get_info_for_week():
		week = get_subha_week()
		return week


