import csvmapper
import json

mapper = csvmapper.DictMapper([
	[
		{'name': 'number'},
		{'name': 'name'},
		{'name': 'schedule_url'},
		{'name': 'image_url'},
		{'name': 'is_done'},
		{'name': 'omit'}
	]
])

built = csvmapper.CSVParser("http://eternityready.com/channel-guide/data/channels_corrected.csv", mapper).buildDict()

output = {'channels': built}

for chan in output["channels"]:

	split = chan["name"].split("#")
	if len(split) > 1:
		chan["name"] = split[0].strip()

output["channels"] = [chan for chan in output["channels"] if not chan["omit"] == "omit"]

print json.dumps(output, indent=4)
