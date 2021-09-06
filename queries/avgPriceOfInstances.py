import pandas as pd
import pymongo
import matplotlib.pyplot as plt

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from globals import REGIONS


mydb = pymongo.MongoClient("mongodb://localhost:27017/").aws_spot

df = pd.DataFrame([])

df1 = pd.DataFrame([])

# input variable
os = "Windows"

for region in REGIONS:
    mycol = mydb[region]
    mydoc = mycol.aggregate([ 
        {"$match": {"os": os } },
        {"$project": { "region": { "$concat": ["$region.endpoint", "-", "$region.zone"] },
         "os": "$os", "price" : "$price"}} ])
    
    df1 = pd.DataFrame(list(mydoc))

    df = df.append(df1)

df = df[["region", "price"]]

df = df.groupby("region").mean().reset_index()

df = df.rename(columns={"region": "Region", "price": "Average Price"})


fig = plt.figure(figsize = (10, 5))
plt.bar(df["Region"], df["Average Price"], width = 0.4)
plt.xticks(rotation=90)
plt.xlabel("Region")
plt.ylabel("Average Price")
plt.title("Average price of Instances using " + os + " Operating System Across Different Regions")
plt.show()
