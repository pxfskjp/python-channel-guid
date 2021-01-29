import bottle
from bottle import route, run, template, static_file, response
import json

import datetime
from datetime import date

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import pickle

bottle.debug(True)

print ""

days = []
days_js = []


schedules = {
	# "46":{},
	# "50": {
	# 	# "2015-09-22": [
	# 	# 	{
	# 	# 		"program_name": "Test Hour-long Show",
	# 	# 		"episode_name": "Season 4 Episode 2",
	# 	# 		"date": "2015-09-23",
	# 	# 		"starts": "0000",
	# 	# 		"duration": 60,
	# 	# 		"info_link": "http://somewhere"
	# 	# 	},
	# 	# 	{
	# 	# 		"program_name": "Test 30min Show",
	# 	# 		"episode_name": "Season 1 Episode 1",
	# 	# 		"date": "2015-09-23",
	# 	# 		"starts": "0100",
	# 	# 		"duration": 30,
	# 	# 		"info_link": "http://somewhere"
	# 	# 	},
	# 	# ]
	# }
}


def add_ordinal(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))





with open("./data/channels_corrected.json") as channels_file:
	channels = json.load(channels_file)

@route('/update')
def update_data():
	global schedules
	global days
	global days_js

	with open('./cache/days.pickle', 'rb') as days_handle:
		days_data = pickle.load(days_handle)
		days = days_data["days"]
		days_js = days_data["days_js"]

	with open('./cache/schedule.pickle', 'rb') as sched_handle:
		schedules = pickle.load(sched_handle)

@route('/days')
def get_days():
	response.content_type = 'application/json'
	return json.dumps(days_js)


@route('/channels')
def get_channels():
	return channels


@route('/schedule/<channel:int>/<date>')
def get_schedule(channel, date):
	# if channel != 50:
	# 	channel = 50
	response.content_type = 'application/json'
	try:
		return json.dumps(schedules[str(channel)][date])
	except KeyError:
		return {"error": "yes"}


@route('/')
def index():
	return template('index')


@route('/static/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='static')

update_data()
run(host='0.0.0.0', port=8080, reloader=False)




print "exit"


