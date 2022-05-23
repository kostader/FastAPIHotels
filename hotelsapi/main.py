from fastapi import FastAPI
from hotelsapi.routers import hotel
from hotelsapi import models
from . import models
from .database import engine
from .routers import hotel, user, auth

from hotelsapi import database

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotels API")

app.include_router(hotel.router)
app.include_router(user.router)
app.include_router(auth.router)
