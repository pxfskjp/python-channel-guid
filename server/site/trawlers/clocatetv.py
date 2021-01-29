import common
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


def unix_time(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta = dt - epoch
	return total_secs(delta)



URL="http://www.locatetv.com/listings/"

def get_locatetv_date(the_date, offset, network_name):
	date_string = the_date.strftime("%Y%m%d")
	req = urllib2.Request(URL + network_name + "?offset=" + str(offset) + "&_=" +  str(unix_time(datetime.datetime.combine(the_date, datetime.time.min))) + "0000"     )
	req.add_header("X-Requested-With", "XMLHttpRequest")
	req.add_header("Cookie", "ab_group_undertone_20140902=005669046f9063c38ec0d9a141ad7937856caf4bs%3A7%3A%22group_b%22%3B; CookieDirectiveAcceptance=4f510adf6828c51508177d1d55afee2f7beed8edi%3A255%3B; country=cbeffaeca60d155b742ade293e28400a3a99de10s%3A2%3A%22US%22%3B; zip=8fe3796d78e8bfab8d0933e24d3fb02666ff20d1s%3A5%3A%2290210%22%3B; headend=b0225f283a584b1ae84cb5097fde0f39673a4374s%3A4%3A%225497%22%3B; version=3f1ff0ceb4fc7754d3f785b1ab5ef4e9921b5244i%3A3%3B")
	response = urllib2.urlopen(req)
	output = response.read()

	soup = BeautifulSoup(output)
	# print soup
	# return

	items = soup.findAll('li', attrs={'class':'schedTv'})

	programs = []

	for item in items:
		# print item
		#return
		prog_time = item.find("ul").findAll("li")[0].text
		desc = item.find("ul").findAll("li")[1].find("div").find("a").text.replace("&#039;", "'")

		try:
			ptime = datetime.datetime.combine(the_date, datetime.datetime.strptime( prog_time  ,  "%I:%M%p"    ).time())
		except Exception:
			continue
			if prog_time.find("mins") == -1:
				continue
			if prog_time.find("ago"):
				mode = -1
			else:
				mode = 1
			mins = int(filter(unicode.isdigit, prog_time)) * mode
			ptime = datetime.datetime.combine(the_date, datetime.datetime.now().time()) - datetime.timedelta(minutes=mins)

		# if ptime.hour < 3:
		#     	continue
		# ptime = ptime - datetime.timedelta(hours=3)

		time_str = ptime.strftime("%H%M")

		programs.append({ "date": the_date.strftime("%Y-%m-%d"), "starts": time_str, "starts_datetime": ptime, "program_name": desc })


	for _ in range(2):
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

# print get_locatetv_date(date.today(), "smile-of-a-child")

class TrawlerLocateTV(Trawler):
	@staticmethod
	def get_info_for_days(days, network_name="smile-of-a-child"):
		schedule = {}
		# yesterday = date.today()-datetime.timedelta(days=1)
		# schedule.update( {yesterday.strftime("%Y-%m-%d"): get_locatetv_date(yesterday, network_name)})
		today = datetime.date.today()
		for d in range(7):
			day = today + datetime.timedelta(days=d)
			schedule.update( {day.strftime("%Y-%m-%d"): get_locatetv_date(day, d, network_name)})

		common.correct_timezone_offsets(schedule)
		# print schedule
		return schedule

# days=[]
# today = datetime.date.today()

# for d in range(7):
# 	days.append(today + datetime.timedelta(days=d))
# days = [today+ datetime.timedelta(days=1)]
# print TrawlerLocateTV.get_info_for_days(days, "smile-of-a-child-network")
