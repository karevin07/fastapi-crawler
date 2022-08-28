from typing import List

import motor.motor_asyncio

MONGO_HOT_URL = "mongodb://root:123456@127.0.0.1:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_HOT_URL)

database = client["591"]

collection = database.get_collection("item_detail")


def house_helper(house) -> dict:
    del house["_id"]
    house["url"] = "https://rent.591.com.tw/home/" + str(house["post_id"])
    return house


# crud operations

# Retrieve all houses in the database

async def retrieve_houses(limit: int):
    houses = []
    if limit == -1:
        async for house in collection.find().limit(limit):
            houses.append(house_helper(house))
    else:
        async for house in collection.find():
            houses.append(house_helper(house))
    return houses


# Retrieve a house item with a matching post_id
async def retrieve_house_by_id(post_id: str) -> dict:
    house = await collection.find_one({"post_id": int(post_id)})
    if house:
        return house_helper(house)


# Retrieve a house with a matching phone number
async def retrieve_house_by_mobile(mobile: str) -> list[dict]:
    houses = []
    async for house in collection.find({"mobile": {"$regex": mobile}}):
        houses.append(house_helper(house))
    return houses


# Retrieve houses with a matching region
async def retrieve_house_by_region(region_id: int) -> list[dict]:
    houses = []
    async for house in collection.find({"region_id": region_id}):
        houses.append(house_helper(house))
    return houses


# Retrieve houses with a matching role
async def retrieve_house_by_role(role: bool, limit: int) -> list[dict]:
    houses = []
    if role:
        if limit == -1:
            async for house in collection.find({"role": 1}):
                houses.append(house_helper(house))
        else:
            async for house in collection.find({"role": 1}).limit(limit):
                houses.append(house_helper(house))
    else:
        if limit == -1:
            async for house in collection.find({"role": {"$ne": 1}}):
                houses.append(house_helper(house))
        else:
            async for house in collection.find({"role": {"$ne": 1}}).limit(limit):
                houses.append(house_helper(house))
    return houses


# Retrieve houses with multiple conditions
async def retrieve_house_by_multi_condition(conditions: dict) -> list[dict]:
    houses = []
    criteria = []
    for k, v in conditions.items():
        if v is None:
            continue
        if k == "region_id":
            c = {"region_id": v}
            criteria.append(c)
        elif k == "allow_gender":
            c = {"allow_gender": k}
            criteria.append(c)
        elif k == "owner_gender":
            c = {"owner_gender": v}
            criteria.append(c)
        elif k == "owner_last_name":
            c = {"owner_last_name": f"/{v}/"}
            criteria.append(c)

    query = {
        "$or": criteria
    }
    async for house in collection.find(query):
        houses.append(house_helper(house))
    return houses
