from typing import Sequence
from pydantic import BaseModel


class Hotel(BaseModel):
    # hotel_id: int
    hotel_name: str


class HotelFindResult(BaseModel):
    results: Sequence[Hotel]


class HotelCreate(BaseModel):
    hotel_name: str
