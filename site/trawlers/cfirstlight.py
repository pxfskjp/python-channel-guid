
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



URL="http://www.firstlight.org.nz/schedule/"

def get_firstlight_date(the_date):
	date_string = the_date.strftime("%d/%m/%Y")
	data = urllib.urlencode({'event_schedule_additional[ed_date]:' : date_string})
	response = urllib2.urlopen(URL, data=data)
	try:
		output = response.read()
	except urllib.error.URLError:
		return []
	soup = BeautifulSoup(output)

	table = soup.findAll('table', attrs={'class':'schedule_list sortable'})[0]

	table_body = table.find('tbody')
	# print table_body

	rows = table_body.findAll('tr')


	programs = []

	for row in rows:
	    cols = row.findAll('td')
	    ptime = datetime.datetime.combine(the_date, datetime.datetime.strptime( cols[0].text  ,  "%I:%M %p"    ).time())
	    time_str = ptime.strftime("%H%M")

	    link = cols[1].text
	    
	    programs.append({ "date": the_date.strftime("%Y-%m-%d"), "starts": time_str, "starts_datetime": ptime, "program_name": link })


	length = len(programs)
	for index, prog in enumerate(programs):
		if index == length - 1:
			next_prog = {"starts_datetime": datetime.datetime.combine(the_date + datetime.timedelta(days=1), datetime.datetime.min.time()) }
		else:
			next_prog = programs[index+1]

		duration = next_prog["starts_datetime"] - prog["starts_datetime"]
		durmins = int(total_secs(duration)/60)
		# print "this: " + str(prog["starts_datetime"]) + ", next: " + str(next_prog["starts_datetime"])
		# print durmins
		programs[index]["duration"] = durmins

	for prog in programs:
		del prog["starts_datetime"]

	# print programs

	return programs

	# print programs

	# # with open("../data/testdata") as data_file:
	# # 	data = json.load(data_file)

	# programs = []







	# for program in data["programs"]:
	# 	p_datetime = datetime.datetime.strptime(program["UserFullDateTime"].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
	# 	# print p_datetime
	# 	# print program["Series"] + "," + program["UTCDateTime"] + "," + program["Duration"]


	# 	durparts = program["Duration"].split(":")

	# 	minutes = (int(durparts[0])*60) + (int(durparts[1]))

	# 	program = {"program_name": program["Series"], "date": p_datetime.strftime("%Y-%m-%d"), "starts": p_datetime.strftime("%H%M"), "duration": minutes}
	# 	programs.append(program)

	# #print data["programs"][0]
	# return programs


	# with open("3abn_test") as html:
	# 	soup = BeautifulSoup(html)
	# table = soup.findAll(attrs={"class": "daily_schedule"})
	# print table[0].text

# get_3abn_date("2015-09-21")

# print get_firstlight_date(date.today())

class TrawlerFirstlight(Trawler):
	@staticmethod
	def get_info_for_days(days):
		schedule = {}
		for day in days:
			schedule.update( {day.strftime("%Y-%m-%d"): get_firstlight_date(day)})

		# print schedule
		return schedule

