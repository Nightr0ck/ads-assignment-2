import pandas as pd
import pymongo

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from globals import REGIONS


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["aws_spot_by_region"]


df = pd.DataFrame([])

df1 = pd.DataFrame([])

# input variable
os = "Windows"

for region in REGIONS:
    mycol = mydb[region]
    mydoc = mycol.aggregate([ { 
    "$project": { "region": { "$concat": ["$region.endpoint", "-", "$region.zone"] }, "os": "$os", "price" : "$price"}}, 
    {"$match":
    {"os": os } } ])
    
    df1 = pd.DataFrame(list(mydoc))

    df = df.append(df1)

df = df[["region", "price"]]

df = df.groupby("region").mean().reset_index()

df = df.rename(columns={"region": "Region", "price": "Average Price"})

print("Average price of Instances using " + os + " Operating System Across Different Regions")
print(df)


