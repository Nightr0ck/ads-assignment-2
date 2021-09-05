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
        instance_type_split = instance_type.split(".")
        size_list = family_size_dict.get(instance_type_split[0], [])
        size_list.append(instance_type_split[1])
        family_size_dict[instance_type_split[0]] = size_list

    for family_size in family_size_dict.items():
        family = family_size[0]
        sizes = family_size[1]

        db[region].insert_one({
            "family": family,
            "spot_instance": []
        })

        for size in sizes:
            db[region].update_one(
                {"family": family},
                {"$push": {"spot_instance": {"size": size, "listings": []}}}
            )
    

    for index, row in df.iterrows():
        date, time = row["timestamp"].split(" ")
        family, size = row["instance_type"].split(".")
        os = row["os"]
        availability_zone = row["region"].split("-")[2]
        price = row["price"]

        print(db[region].find(
            {"family": family}
            #{"$push": {"spot_instance.listings": {"date": date, "time": time, "os": os, "availability_zone": availability_zone, "price": price}}}
        ).next())



