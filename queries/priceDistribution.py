import pymongo
import pandas as pd
import matplotlib.pyplot as plt

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from globals import REGIONS

db = pymongo.MongoClient("mongodb://localhost:27017/").aws_spot
results = db[REGIONS[0]].find({"$and": [{"instance_type.family": "m4"}, {"instance_type.size": "16xlarge"}, {"os": "SUSE Linux"}]}, {"timestamp": 1, "price": 1})
df = pd.DataFrame.from_records(results).drop(columns=["_id"])

def hour(timestamp):
    time = timestamp.split(" ")[1]
    hour, minutes = time.split(":")[:2]
    return int(hour) + ((int(minutes) / 60))

df["time"] = df["timestamp"].apply(hour)
df.drop(columns=["timestamp"], inplace=True)
print(df)

fig = plt.figure(figsize = (15, 5))
plt.scatter(df["time"], df["price"], s=5)
plt.xlabel("Time")
plt.xticks(range(0, 25), ["0000", "0100", "0200", "0300", "0400", "0500", "0600", "0700", "0800", "0900", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2000","2100", "2200", "2300", "2400"])
plt.ylabel("Price")
plt.savefig("test.png")