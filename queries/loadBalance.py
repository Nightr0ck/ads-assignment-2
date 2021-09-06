import pandas as pd
import pymongo

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from globals import REGIONS

db = pymongo.MongoClient("mongodb://localhost:27017/").aws_spot
#docs = db[REGIONS[6]].find({"$and": [{"instance_type.family": "m3"}, {"instance_type.size": "large"}]}, {"price": 1, "region.zone": 1})

# input data
region = "eu_west_1"
family = "m3"
size = "large"

# mongo query
docs = db[region].aggregate([
    {"$match": { "$and": [{"instance_type.family": "m3"},
                          {"instance_type.size": "large"}]}
    },
    {"$project": { "zone": { "$concat": ["$region.zone"] }, "price" : "$price"}} ])

# aggregating the data in Python
df = pd.DataFrame(list(docs))
df = df[["zone", "price"]]
df = df.groupby("zone").mean().reset_index()
df = df.rename(columns={"zone": "Zone", "price": "Average Price"})

print(f'The average price of {family} ({size}) instances in {region} according to zones')
print(df)