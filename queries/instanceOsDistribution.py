import pandas as pd
import pymongo
import matplotlib.pyplot as plt

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from globals import REGIONS

mydb = pymongo.MongoClient("mongodb://localhost:27017/").aws_spot

# input variable
region = "ap_northeast_1"
mycol = mydb[region]

# query os column only from mongodb
mydoc = mycol.aggregate([
    {"$project": { "os": { "$concat": ["$os"] }}},
    {"$group" : {"_id":"$os", "count":{"$sum":1}}},
    {"$sort": { "count" : -1 }}
])

# convert retrieved data to dataFrame
df = pd.DataFrame(list(mydoc))

# rename the columns name
df = df.rename(columns={"_id": "OS", "count": "Number of Instances"})

# set size for graph
fig = plt.figure(figsize = (10, 5))

# plot graph
plt.bar(df["OS"], df["Number of Instances"], width = 0.4)

# naming the x axis 
plt.xlabel("OS")

# naming the y axis
plt.ylabel("Number of Instances")

# title of graph
plt.title("Instance OS distribution in " + region)

# show graph
plt.show()