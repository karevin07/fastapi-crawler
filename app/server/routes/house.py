from typing import Union

from fastapi import APIRouter, Body, Query, Depends

from ..database import (
    retrieve_house_by_id,
    retrieve_houses,
    retrieve_house_by_mobile,
    retrieve_house_by_role
)
from ..models.house import (
    ErrorResponseModel,
    ResponseModel,
    HouseSchema
)

router = APIRouter()


class RegionQueryPatams:
    def __init__(self, region_id: int = Query(None, description="taipei = 1, new_taipei = 3"), ):
        self.region_id = region_id


#
@router.get("/", response_description="Houses retrieved")
async def get_all_houses():
    houses = await retrieve_houses(limit=10)
    if houses:
        return ResponseModel(houses, "House data retrieved successfully")
    return ResponseModel(houses, "Empty list returned")


@router.get("/items/{id}", response_description="House data retrieved by id")
async def get_house_data_by_id(post_id):
    house = await retrieve_house_by_id(post_id)
    if house:
        return ResponseModel(house, "House data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "House doesn't exist.")


@router.get("/mobile/{mobile}", response_description="House data retrieved by phone number")
async def get_house_data_by_mobile(mobile):
    house = await retrieve_house_by_mobile(mobile)
    if house:
        return ResponseModel(house, "House data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "House doesn't exist.")


@router.get("/region/{region_id}")
async def get_house_data_by_region(
        region_id: int = Query(..., description="taipei = 1, new_taipei = 3"),
        allow_gender: Union[int, None] = None,
        owner_gender: Union[int, None] = None,
        owner_last_name: Union[str, None] = None):

    print({"region_id": region_id, "allow_gender": allow_gender, "owner_gender": owner_gender, "owner_last_name": owner_last_name})
    if allow_gender:
        return {"region_id": region_id, "allow_gender": allow_gender}
    return region_id


@router.get("/role/{role_bool}")
async def get_house_data_by_role(role_bool: bool, limit: int = 10):
    house = await retrieve_house_by_role(role_bool, limit)
    if house:
        return ResponseModel(house, "House data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "House doesn't exist.")
