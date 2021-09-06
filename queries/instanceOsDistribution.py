import pandas as pd
import pymongo
import matplotlib.pyplot as plt
from globals import REGIONS

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["aws_spot_by_region"]


region = "ap_northeast_1"
mycol = mydb[region]

mydoc = mycol.find().limit(200)

df = pd.DataFrame(list(mydoc))

df = df["os"].value_counts().rename_axis('OS').reset_index(name='Number of Instances')

fig = plt.figure(figsize = (10, 5))
plt.bar(df["OS"], df["Number of Instances"], width = 0.4)
 
plt.xlabel("OS")
plt.ylabel("Number of Instances")
plt.title("Instance OS distribution in " + region)
plt.show()