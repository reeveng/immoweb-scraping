import requests
import json

file_name = "results.json"
content_size = 500
page_index = 1

with open(file_name, "r") as infile:
    data = json.load(infile)
    data = data


# for house in data:
    # figure out how a thing looks
    # filter on:
    # - price
    # - bedrooms
    # - energy consumption
