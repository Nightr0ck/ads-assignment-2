import pymongo
import pandas as pd
from globals import REGIONS
from datetime import datetime

db = pymongo.MongoClient("mongodb://localhost:27017/")
db.drop_database("aws_spot")
db = db.aws_spot

def family_size(instance_type):
    family, size = instance_type.split(".")
    return {"family": family, "size": size}

def endpoint_zone(region):
    end1, end2, zone = region.split("-")
    return {"endpoint": end1 + "-" + end2, "zone": zone}

def datetime_object(timestamp):
    date, time = timestamp.split(" ")
    year, month, day = date.split("-")
    hour, minute, second = time.split(":")[:3]
    second = second.split("+")[0]

    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

for region in REGIONS:
    df = pd.read_csv("./data/" + region.replace("_", "-") + ".csv", header=None)
    df.rename(columns={0:"timestamp", 1:"instance_type", 2:"os", 3:"region", 4:"price"}, inplace=True)
    df["timestamp"] = df["timestamp"].apply(datetime_object)
    df["instance_type"] = df["instance_type"].apply(family_size)
    df["region"] = df["region"].apply(endpoint_zone)
    print(df.head(5))
    print("converting dataframe into dictionary")
    data = df.to_dict(orient="records")
    print("inserting into " + region)
    db[region].insert_many(data)
    print("inserted")

#{"datetime": datetime object, instance_type:{{"family": family}, {"size", size}}, "os": os, "region":{{"endpoint": endpoint}, {"zone": zone}}, "price": price}