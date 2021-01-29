import urllib2
import re
import json
import datetime
from datetime import date

from trawlers import c3abn

import itertools

days = []

with open("../data/days.json", "w+") as days_file:

	today = datetime.date.today()

	for d in range(7):
		days.append(today + datetime.timedelta(days=d)) 

	for day in days:
		print day

# with open("../data/channels.json") as channels_file:
# 	channels = json.load(channels_file)

print c3abn.Trawler3ABN.get_info_for_days(days)