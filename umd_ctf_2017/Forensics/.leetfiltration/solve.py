#!/usr/bin/python3

import os

os.system("tshark -r capture.cap -x | grep \"13\" | grep -v \"88\" | grep -v \"@\" > temp.txt")


data = []

with open("temp.txt", "r") as f:
    data = f.read().split("\n")

decoded = ""
for line in data:
    if "37" in line:
        decoded += "1"
    else:
        decoded += "0"

print(decoded[0:2] + "11110" + decoded[3:])
