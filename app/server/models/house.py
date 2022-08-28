from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class HouseSchema(BaseModel):
    post_id: int = Field()
    title: str = Field()
    region: str = Field()
    section: str = Field()
    kind: str = Field()
    region_id: int = Field()
    section_id: int = Field()
    kind_id: int = Field()
    area: str = Field()
    floor: str = Field()
    shape: str = Field()
    address: str = Field()
    role_name: str = Field()
    role: str = Field()
    name: str = Field()
    mobile: str = Field()
    price: int = Field()
    owner: int = Field()
    allow_gender: int = Field()

    class Config:
        schema_extra = {
            "example": {
                'post_id': 13002110,
                'title': '（天母新光三越正後面電梯套房（有獨立陽台',
                'region': '台北市',
                'section': '士林區',
                'kind': '獨立套房',
                'area': '8坪',
                'floor': '2F/10F',
                'shape': '電梯大樓',
                'address': '士林區天母東路',
                'role_name': '代理人',
                'role': 2,
                'name': '林太太',
                'mobile': '0986851077',
                'price': 13500,
                'owner': '0',
                'allow_gender': 2
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
