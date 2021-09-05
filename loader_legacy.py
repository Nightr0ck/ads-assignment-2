import pymongo
import pandas as pd

mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
awsSpotRaw = mongoClient["aws_spot_raw"]
apNortheast = awsSpotRaw["ap_northeast"]

df = pd.read_csv("./data/ap-northeast-1.csv", header=None)
df.rename(columns={0:"timestamp", 1:"instance_type", 2:"os", 3:"region", 4:"price"}, inplace=True)
print(df.head(5))
data = df.to_dict(orient="records")
apNortheast.insert_many(data)