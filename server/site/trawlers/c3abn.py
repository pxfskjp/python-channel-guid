
from .common import Trawler

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import json
import datetime
from datetime import date


def total_secs(delta):
	return (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10**6) / 10**6


URL="http://3abn.org/sabramedia/controller/read-schedule-xml.php?"

def get_3abn_date(the_date, abn_network_id):
	date_string = the_date.strftime("%Y-%m-%d")
	# print date_string
	encoded=urllib.urlencode({
		"action": "init",
		"date": date_string,
		"network": abn_network_id,
		"search": "",
		"local_timezone":"America/Los Angeles", #"Europe/London",
		"tz_offset": "0" #"-60"
	})
	# print encoded

	response = urllib2.urlopen(URL + encoded)
	output = response.read()
	data = json.loads(output)

	# with open("../data/testdata") as data_file:
	# 	data = json.load(data_file)

	programs = []
	if not data["programs"]:
		return []

	for program in data["programs"]:
		p_datetime = datetime.datetime.strptime(program["UserFullDateTime"].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
		# print p_datetime
		# print program["Series"] + "," + program["UTCDateTime"] + "," + program["Duration"]


		durparts = program["Duration"].split(":")

		minutes = (int(durparts[0])*60) + (int(durparts[1]))

		program = {"program_name": program["Series"], "episode_name": program["Content"], "date": p_datetime.strftime("%Y-%m-%d"), "starts": p_datetime.strftime("%H%M"), "duration": minutes}
		programs.append(program)

	#print data["programs"][0]
	return programs


	# with open("3abn_test") as html:
	# 	soup = BeautifulSoup(html)
	# table = soup.findAll(attrs={"class": "daily_schedule"})
	# print table[0].text

# get_3abn_date("2015-09-21")



class Trawler3ABN(Trawler):
	@staticmethod
	def get_info_for_days(days, abn_network_id=1):
		schedule = {}
		for day in days:
			# print day.strftime("%Y-%m-%d")
			schedule.update( {day.strftime("%Y-%m-%d"): get_3abn_date(day, abn_network_id)})
		return schedule


# print Trawler3ABN.get_info_for_days([datetime.date.today()])