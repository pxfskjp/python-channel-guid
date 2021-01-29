import urllib
import csv

grabber = urllib.URLopener()

with open("http://eternityready.com/channel-guide/data/obs/channels.csv", "rb") as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		number = row[0]
		image_url = row[3]
		#grabber.retrieve(image_url, "img/channel_logos/" + number + ".jpg")
# testfile = urllib.URLopener()
# testfile.retrieve("http://randomsite.com/file.gz", "file.gz")