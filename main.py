from gettext import install
from fastapi import FastAPI, APIRouter


HOTELS = [
    {
        "id": 1,
        "hotel_name": "Miboo"
    },
    {
        "id": 2,
        "hotel_name": "Feedfire"
    },
    {
        "id": 3,
        "hotel_name": "Meevee"
    },
    {
        "id": 4,
        "hotel_name": "Jazzy"
    },
    {
        "id": 5,
        "hotel_name": "Linkbuzz"
    }
]

app = FastAPI(title="Hotels API")

main = APIRouter()


@main.get("/")
async def root():
    return {"Message": "Hello world"}


@main.get("/hotel/{hotel_id}")
async def hotel_info(hotel_id: int, status_code=200):
    result = [hotel for hotel in HOTELS if hotel["id"] == hotel_id]
    if result:
        return result[0]


@main.get("/hotel/seatch")
async def find_hotel(name: str | None = None, max_result: int = 10):
    return {"result": max_result}


app.include_router(main)
