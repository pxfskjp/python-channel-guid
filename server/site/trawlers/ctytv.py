
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


URL="http://www.tytvonline.com/"

BY_DAYS = ["schedule", "tue", "wed", "thur", "fri", "sat", "sun"]

def get_ty_day(date):
	# print date
	response = urllib2.urlopen(URL + BY_DAYS[date.weekday()] + ".html")
	output = response.read()
	soup = BeautifulSoup(output)
	# print soup
	table = soup.findAll('table')[0]

	rows = table.findAll('tr')[1:]
	days_programs = []

	for row in rows:
		ptime = datetime.datetime.combine(date, datetime.datetime.strptime( row.findAll('th')[0].text,  "%I:%M %p"    ).time())
		if ptime.hour < 0:
			continue
		ptime = ptime - datetime.timedelta(hours=-2)
		descs = row.findAll('td')
		desc = "prev"
		if len(descs) > 0:
			desc = row.findAll('td')[0].text.replace("&quot;", '"')
		# print str(date) + ", " + desc
		time_str = ptime.strftime("%H%M")
		days_programs.append({ "date": date.strftime("%Y-%m-%d"), "starts": time_str, "starts_datetime": ptime, "program_name": desc })



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


def get_ty_week():
	schedule = {}

	today = datetime.date.today()
	days_since_monday = today.weekday()
	monday = today - datetime.timedelta(days=days_since_monday)
	for i in range(0, 7):
		date = monday + datetime.timedelta(days=i)
		schedule[date.strftime("%Y-%m-%d")] = get_ty_day(date)
	
	# print schedule
	return schedule


class TrawlerTY(Trawler):
	@staticmethod
	def get_info_for_week():
		week = get_ty_week()
		return week


