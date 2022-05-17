from fastapi import FastAPI, APIRouter, Query
from hotelsapi.hotels_data import HOTELS
from hotelsapi.schemas import Hotel, HotelFindResult, HotelCreate

app = FastAPI(title="Hotels API")

main = APIRouter()


@main.get("/")
async def root():
    return {"Message": "Hello world"}


@main.get("/hotel/{hotel_id}", status_code=200, response_model=Hotel)
async def hotel_info(hotel_id: int):
    result = [hotel for hotel in HOTELS if hotel["id"] == hotel_id]
    if result:
        return result[0]


@main.get("/search/", status_code=200, response_model=HotelFindResult)
def search_hetels(*, keyword: str | None = Query(None, min_length=3, example="Jazzy"), max_results: int | None = 10):
    if not keyword:
        return {"results": HOTELS[:max_results]}

    results = filter(lambda hotel: keyword.lower()
                     in hotel["hotel_name"].lower(), HOTELS)
    return {"results": list(results)[:max_results]}

# New addition, using Pydantic model `RecipeCreate` to define
# the POST request body


@main.post("/recipe/", status_code=201, response_model=Hotel)
def create_recipe(*, hotel_name: HotelCreate) -> dict:
    """
    Create a new recipe (in memory only)
    """
    new_entry_id = len(HOTELS) + 1
    hotel_entry = Hotel(
        hotel_id=new_entry_id,
        hotel_name=hotel_name.hotel_name
    )
    HOTELS.append(hotel_entry.dict())

    return hotel_entry


app.include_router(main)
