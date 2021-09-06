import pymongo
import matplotlib.pyplot as plt
from globals import REGIONS

db = pymongo.MongoClient("mongodb://localhost:27017/").aws_spot
docs = db[REGIONS[3]].find({"$and": [{"instance_type.family": "m3"}, {"instance_type.size": "large"}, {"os": "Linux/UNIX"}, {"region.zone": "1a"}]}, {"price": 1, "timestamp": 1}).sort("timestamp", 1)

timestamp = []
prices = []

for doc in docs:
    timestamp.append(doc["timestamp"])
    prices.append(doc["price"])

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