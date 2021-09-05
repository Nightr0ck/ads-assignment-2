import pymongo
import pandas as pd
from globals import REGIONS

db = pymongo.MongoClient("mongodb://localhost:27017/")
db.drop_database("aws_spot_by_region")
db = db.aws_spot_by_region

for region in REGIONS:
    df = pd.read_csv("./data/" + region.replace("_", "-") + ".csv", header=None)
    df.rename(columns={0:"timestamp", 1:"instance_type", 2:"os", 3:"region", 4:"price"}, inplace=True)

    family_size_dict = {}
    for instance_type in df["instance_type"].unique():
        family, size = instance_type.split(".")
        db[region].insert_one({
            "family": family,
            "size": size,
            "spot_instance": []
        })
    
    family_size_index = pymongo.IndexModel([("family", pymongo.ASCENDING), ("size", pymongo.ASCENDING)])
    db[region].create_indexes([family_size_index])
    

    for index, row in df.iterrows():
        date, time = row["timestamp"].split(" ")
        family, size = row["instance_type"].split(".")
        os = row["os"]
        availability_zone = row["region"].split("-")[2]
        price = row["price"]

        print(index)

        db[region].update_one(
            {"family": family, "size": size},
            {"$push": {"spot_instance": {"date": date, "time": time, "os": os, "availability_zone": availability_zone, "price": price}}}
        )



