from fastapi import Depends, APIRouter, Query, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, oauth2
from ..schemas import hotels
from ..database import get_db

from typing import List

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("", response_model=List[hotels.Hotel])
def get_hotels(db: Session = Depends(get_db), limit: int = 5, skip: int = 0):
    # cursor.execute(""" SELECT * FROM hotels """)
    # hotels = cursor.fetchall()
    hotels = db.query(models.Hotel).limit(limit).offset(skip).all()

    return hotels


@router.post("", status_code=status.HTTP_201_CREATED, response_model=hotels.Hotel)
def create_hotel(hotel: hotels.HotelCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO  hotels (name, city, open_date, number_rooms) VALUES (%s, %s, %s, %s) RETURNING * """,
    #                (hotel.name, hotel.city, hotel.open_date, hotel.number_rooms))
    # new_hotel = cursor.fetchone()
    # conn.commit()
    new_hotel = models.Hotel(added_by=current_user.id, **hotel.dict())
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel


@router.get("/{id}", status_code=200, response_model=hotels.Hotel)
def get_hotel(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """SELECT * FROM hotels WHERE hotel_id = %s""", (str(hotel_id),))
    # hotel = cursor.fetchone()

    hotel = db.query(models.Hotel).filter(models.Hotel.id == id).first()

    if not hotel:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Hotel with ID {id} not foound")
    return hotel


@router.put("/{id}", response_model=hotels.Hotel)
def update_hotel(id: int, updated_hotel: hotels.HotelCreate, db: Session = Depends(get_db),   current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE hotels SET name =  %s, city= %s, open_date = %s, number_rooms = %s WHERE id = %s RETURNING *""",
    #                (hotel.name, hotel.city, hotel.open_date, hotel.number_rooms, str(id)))
    # updated_hotel = cursor.fetchone()
    # conn.commit()

    hotel_query = db.query(models.Hotel).filter(models.Hotel.id == id)
    hotel = hotel_query.first()

    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with ID {id} not found")

    hotel_query.update(updated_hotel.dict(), synchronize_session=False)
    db.commit()

    return hotel_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_hotel(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM hotels WHERE id =  %s RETURNING * """,
    #                (str(id),))
    # deleted_hotel = cursor.fetchone()
    # conn.commit()

    hotel = db.query(models.Hotel).filter(models.Hotel.id == id)

    if not hotel.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with ID {id} not found")

    hotel.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
