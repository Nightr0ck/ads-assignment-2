import pandas as pd
import pymongo
from globals import REGIONS


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["aws_spot_by_region"]


df = pd.DataFrame([])

df1 = pd.DataFrame([])

for region in REGIONS:
    mycol = mydb[region]
    mydoc = mycol.aggregate([ { 
    "$project": { "region": { "$concat": ["$region.endpoint", "-", "$region.zone"] }, "os": "$os", "price" : "$price"}}, {"$limit": 100} ])
    
    df1 = pd.DataFrame(list(mydoc))

    df = df.append(df1)

# input variable
os = "Windows"

df = df[df["os"] == os]

df = df[["region", "price"]]

df = df.groupby("region").mean().reset_index()

df = df.rename(columns={"region": "Region", "price": "Average Price"})

print("Average price of Instances using " + os + " Operating System Across Different Regions")
print(df)


