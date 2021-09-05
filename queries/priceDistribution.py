import re
from globals import REGIONS
import pymongo
import pandas as pd
from globals import REGIONS

db = pymongo.MongoClient("mongodb://localhost:27017/").aws_spot
results = db[REGIONS[0]].find({"$and": [{"instance_type.family": "m4"}, {"instance_type.size": "16xlarge"}]}, {"price": 1})

prices = []
for result in results:
    prices.append(result["price"])
prices.sort()

first_half = []
second_half = []

if len(prices) % 2 == 0:
    first_half = prices[:int(len(prices)/2) + 1]
    second_half = prices[int(len(prices)/2) + 1 :]
else:
    first_half = prices[:int(len(prices)/2) + 1]
    second_half = prices[int(len(prices)/2) :]

if len(first_half) % 2 == 0:
    lower_quartile = (first_half[int(len(first_half) / 2)] + first_half[int(len(first_half) / 2) + 1]) / 2
    upper_quartile = (second_half[int(len(second_half) / 2)] + second_half[int(len(second_half) / 2) + 1]) / 2
    print(lower_quartile, " - ",  upper_quartile)
else:
    lower_quartile = first_half[int(len(first_half) / 2)]
    upper_quartile = second_half[int(len(second_half) / 2)]
    print(lower_quartile, " - ",  upper_quartile)
