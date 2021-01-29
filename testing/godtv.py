import json
import datetime

with open("237") as f:
	data = json.load(f)
	for a in data["data"]["1443844800"]:
		print a