from typing import Union

from fastapi import APIRouter, Query

from ..database import (
    retrieve_house_by_id,
    retrieve_houses,
    retrieve_house_by_mobile,
    retrieve_house_by_role,
    retrieve_house_data_by_optional_field
)
from ..models.house import (
    ErrorResponseModel,
    ResponseModel
)

router = APIRouter()


@router.get("/", response_description="Houses retrieved")
async def get_all_houses():
    houses = await retrieve_houses(limit=Query(10, description="all = -1"))
    if houses:
        return ResponseModel(houses, "House data retrieved successfully")
    return ResponseModel(houses, "Empty list returned")


@router.get("/id/{post_id}", response_description="House data retrieved by id")
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


@router.get("/items/")
async def get_house_data_by_optional_field(
        region_id: Union[int, None] = Query(None, description="taipei = 1, new_taipei = 3"),
        allow_gender: Union[int, None] = Query(None, description="male = 1, female = 2, male and female = 3"),
        owner_gender: Union[int, None] = Query(None, description="male = 1, female = 2"),
        role: Union[int, None] = Query(None, description="屋主 = 1, 代理人 = 2, 仲介 = 3"),
        name: Union[str, None] = Query(None, description="last name"),
        limit: int = Query(10, description="all = -1")
):

    conditions = {
        "region_id": region_id,
        "allow_gender": allow_gender,
        "owner_gender": owner_gender,
        "name": name,
        "role": role
    }
    house = await retrieve_house_data_by_optional_field(conditions, limit)
    if house:
        return ResponseModel(house, "House data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "House doesn't exist.")


@router.get("/role/")
async def get_house_data_by_role(
        role_bool: bool = Query(..., description="true: 屋主刊登, false: 非屋主"),
        limit: int = Query(10, description="all = -1")):
    house = await retrieve_house_by_role(role_bool, limit)
    if house:
        return ResponseModel(house, "House data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "House doesn't exist.")
