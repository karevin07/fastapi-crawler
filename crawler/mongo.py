from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()
mongo_host = os.environ["MONGO_HOST"]
mongo_port = int(os.environ["MONGO_PORT"])
user = os.environ["MONGO_ROOT_USER"]
password = os.environ["MONGO_ROOT_PASSWORD"]


def get_client():
    client = MongoClient(mongo_host,
                         mongo_port,
                         username=user,
                         password=password
                         )
    return client


def insert_item(item, db_name, collection_name):
    client = get_client()
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(item)


def delete_item(post_id, db_name, collection_name):
    client = get_client()
    db = client[db_name]
    collection = db[collection_name]
    collection.delete_one({'post_id': post_id})


def update_item(item, db_name, collection_name):
    client = get_client()
    db = client[db_name]
    collection = db[collection_name]
    mongo_query = {"post_id": item["post_id"]}
    new_value = {"$set": {"price": item["price"]}}
    collection.update_one(mongo_query, new_value)


def get_item_info(collection):
    item_price = {}
    for x in collection.find():
        item_price[x["post_id"]] = x["price"]
    return item_price
