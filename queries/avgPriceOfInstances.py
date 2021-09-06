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

# loop to append all collections into one dataFrame
for region in REGIONS:
    mycol = mydb[region]

    # concatenate region name and retrieve os and price columns from mongodb
    mydoc = mycol.aggregate([ 
        {"$match": {"os": os } },
        {"$project": { "region": { "$concat": ["$region.endpoint", "-", "$region.zone"] }, "price" : "$price"}} ])
    
    # # convert data retrieved to dataFrame
    df1 = pd.DataFrame(list(mydoc))

    # append data retrieved into the master dataFrame
    df = df.append(df1)

# Group the data by region
df = df.groupby("region").mean().reset_index()

# rename the column name
df = df.rename(columns={"region": "Region", "price": "Average Price"})

print("Average price of Instances using " + os + " Operating System Across Different Regions")
print(df)

# set size for graph
#fig = plt.figure(figsize = (10, 5))

# plot graph
#plt.bar(df["Region"], df["Average Price"], width = 0.4)

# show x axis in vertical
#plt.xticks(rotation=90)

# naming the x axis
#plt.xlabel("Region")

# naming the y axis
#plt.ylabel("Average Price")

# title of graph
#plt.title("Average price of Instances using " + os + " Operating System Across Different Regions")

# show graph
#plt.show()
