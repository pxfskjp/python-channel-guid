
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


URL="http://www.harvesttv.in/schedule"



def get_harvest_day(date, day_name):
	if day_name == "monday":
		return []
	# print date
	response = urllib2.urlopen(URL )#+ BY_DAYS[date.weekday()] + ".html")
	output = response.read()
	soup = BeautifulSoup(output)
	# print soup
	# print day_name
	div = soup.findAll("div", attrs={"id": day_name})[0]
	# print div
	table = div.find('table')#.findAll("tbody")[0]
	# print table

	rows = table.findAll('tr')[1:]
	days_programs = []

	for row in rows:
	    cols = row.findAll('td')
	    ptime = datetime.datetime.combine(date, datetime.datetime.strptime( cols[0].text.replace(" AM", "AM").replace(" PM", "PM")  ,  "%I:%M%p"    ).time())
	    if ptime.date() > date:
	    	continue
	    time_str = ptime.strftime("%H%M")

	    link = cols[2].text
	    
	    days_programs.append({ "date": date.strftime("%Y-%m-%d"), "starts": time_str, "starts_datetime": ptime, "program_name": link })



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


BY_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def get_harvest_week():
	schedule = {}

	today = datetime.date.today()
	days_since_monday = today.weekday()
	monday = today - datetime.timedelta(days=days_since_monday)
	for i in range(0, 7):
		date = monday + datetime.timedelta(days=i)
		schedule[date.strftime("%Y-%m-%d")] = get_harvest_day(date, BY_DAYS[i])
	
	# print schedule
	return schedule


# print get_harvest_day(datetime.date.today(), "thursday")

class TrawlerHarvest(Trawler):
	@staticmethod
	def get_info_for_week():
		week = get_harvest_week()
		return week


