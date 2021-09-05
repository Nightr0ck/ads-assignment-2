import pymongo
import pandas as pd
from globals import REGIONS

#mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
#awsSpotRaw = mongoClient["aws_spot_raw"]
#apNortheast = awsSpotRaw["ap_northeast"]

db = pymongo.MongoClient("mongodb://localhost:27017/")
db.drop_database("aws_spot_by_region")
db = db.aws_spot_by_region

for region in REGIONS:
    df = pd.read_csv("./data/" + region.replace("_", "-") + ".csv", header=None)
    df.rename(columns={0:"timestamp", 1:"instance_type", 2:"os", 3:"region", 4:"price"}, inplace=True)

    #df = pd.read_csv("./data/ap-northeast-1.csv", header=None)
    #df.rename(columns={0:"timestamp", 1:"instance_type", 2:"os", 3:"region", 4:"price"}, inplace=True)
    #print(df.head(5))

    def date(datetime):
        return datetime.split(" ")[0]

    def time(datetime):
        return datetime.split(" ")[1]

    def availability_zone(region):
        return region.split("-")[2]

    for instance_type in df["instance_type"].unique():
        #to_family[instance_type] = instance_type.split(".")[0]
        #to_size[instance_type] = instance_type.split(".")[1]
        filtered = df[df["instance_type"] == instance_type]
        filtered.insert(1, "date", df["timestamp"].apply(date))
        filtered.insert(2, "time", df["timestamp"].apply(time))
        filtered.insert(6, "availability_zone", df["region"].apply(availability_zone))
        filtered.drop(columns=["timestamp", "instance_type", "region"], inplace=True)

        print(filtered.head(5))

        for os in filtered["os"].unique():
            filtered_os = filtered[filtered["os"] == os]
            filtered_os.drop(columns=["os"], inplace=True)

            print(filtered_os.head(5))

            for zone in filtered_os["availability_zone"].unique():
                filtered_zone = filtered_os[filtered_os["availability_zone"] == zone]
                filtered_zone.drop(columns=["availability_zone"], inplace=True)
                data = {"family": instance_type.split(".")[0], "size": instance_type.split(".")[1], "os": os, "availability_zone": zone, "spot_instance": [filtered_zone.to_dict(orient="records")]}
                db[region].insert_many([data])
            
            #data = {"family": instance_type.split(".")[0], "size": instance_type.split(".")[1], "os": os, "spot_instance": [filtered_os.to_dict(orient="records")]}
            #db[region].insert_many([data])
            #print("inserted")

    #suse_linux = filtered[filtered["os"] == "SUSE Linux"]
    #linux_unix = filtered[filtered["os"] == "Linux/UNIX"]
    #windows = filtered[filtered["os"] == "Windows"]

    #data = {"family": instance_type.split(".")[0], "size": instance_type.split(".")[1], "os": "SUSE Linux", "spot_instance": [suse_linux.to_dict(orient="records")]}
    #apNortheast.insert_many([data])
    #print("inserted")

    #dataframes.append(df[df["instance_type"] == instance_type]) #dataframes filtered according to instance_type
    #data = {"family": instance_type.split(".")[0], "size": instance_type.split(".")[1], "spot_instance": [filtered.to_dict(orient="records")]}
    #apNortheast.insert_many([data])
    #print("inserted")
    #master_list.append({"family": instance_type.split(".")[0], "size": instance_type.split(".")[1], "spot_instance": [filtered.to_dict(orient="records")]})

#apNortheast.insert_many(master_list)

#print(dataframes[0])
#df.insert(1, "date", df["timestamp"].apply(date))
#df.insert(2, "time", df["timestamp"].apply(time))
#df.insert(4, "family", df["instance_type"].apply(family))
#df.insert(5, "size", df["instance_type"].apply(size))
#print(df)
#data = df.to_dict(orient="records")
#print(data[0])
#apNortheast.insert_many(data)

#[{"family": "lalal", "size": "lalala", spot_instances: []}]