import urllib
import csv

grabber = urllib.URLopener()

with open("logos_2.txt", "rb") as f:
	for line in f:
		s = line.split(",")
		grabber.retrieve(s[1], "./" + s[0] + ".jpg")
# testfile = urllib.URLopener()
# testfile.retrieve("http://randomsite.com/file.gz", "file.gz")