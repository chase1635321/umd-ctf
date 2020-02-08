import os

with open('strings.txt') as f:
	for line in f:
		os.system("./baby2 " + line.rstrip() + " && echo " + line.rstrip())

