import pandas as pd
import pymongo
import matplotlib.pyplot as plt

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from globals import REGIONS

db = pymongo.MongoClient("mongodb://localhost:27017/").aws_spot
# input variable is the region (collections)
region = REGIONS[3]

# query only the instance family column from mongodb
docs = db[region].aggregate([
    {"$project": { "Instance": { "$concat": ["$instance_type.family"] }}}
])

# convert data retrieved to dataFrame
df = pd.DataFrame(list(docs))

# Get frequency of instance
df = df["Instance"].value_counts().rename_axis("Instance").reset_index(name="Frequency")

# set size for graph
fig = plt.figure(figsize = (10, 5))

# plot graph
plt.bar(df["Instance"], df["Frequency"], width = 0.4)
 
# naming the x axis
plt.xlabel("Instance")

# naming the y axis
plt.ylabel("Frequency")

# title of graph
plt.title("Instance Frequency in " + region)

# show graph
plt.show()