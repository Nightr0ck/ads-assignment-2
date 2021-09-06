import pymongo
import matplotlib
import matplotlib.pyplot as plt

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from globals import REGIONS

db = pymongo.MongoClient("mongodb://localhost:27017/").aws_spot

# input data
region = REGIONS[3]
zone = "1a"
family = "m3"
size = "large"
os = "Linux/UNIX"

docs = db[region].find({"$and": [{"instance_type.family": family}, {"instance_type.size": size}, {"os": os}, {"region.zone": zone}]}, {"price": 1, "timestamp": 1}).sort("timestamp", 1)

timestamp = []
prices = []

for doc in docs:
    timestamp.append(doc["timestamp"])
    prices.append(doc["price"])

fig = plt.figure(figsize = (15, 5))

# plotting the points
plt.plot(timestamp, prices)

# naming the x axis
plt.xlabel('Timestamp')
# naming the y axis
plt.ylabel('Price')

# giving a title to my graph
plt.title('Time-series Graph of AWS Spot Prices (M3 Large, Southeast 1a)')

# function to show the plot
plt.show()
plt.savefig("test.png")