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
docs = db[region].aggregate([
    {"$project": { "Instance": { "$concat": ["$instance_type.family"] }}}
])
#docs = db[region].find({}, {"instance_type.family": 1, "os": 1})

df = pd.DataFrame(list(docs))

df = df["Instance"].value_counts().rename_axis("Instance").reset_index(name="Frequency")

fig = plt.figure(figsize = (10, 5))
plt.bar(df["Instance"], df["Frequency"], width = 0.4)
 
plt.xlabel("Instance")
plt.ylabel("Frequency")
plt.title("Instance Frequency in " + region)
plt.show()