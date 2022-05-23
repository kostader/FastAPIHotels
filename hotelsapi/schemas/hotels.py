from pydantic import BaseModel
from datetime import datetime


class HotelBase(BaseModel):
    name: str
    location: str
    rating: int


class HotelCreate(HotelBase):
    pass


class Hotel(HotelBase):
    id: int
    created_at: datetime
    added_by: int | None

    class Config:
        orm_mode = True
