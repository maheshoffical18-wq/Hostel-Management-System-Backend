# backend/app/routers/rooms.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Room
from ..schemas import RoomResponse


router = APIRouter(
    prefix="/api/rooms",
    tags=["Rooms"]
)


@router.get("/", response_model=list[RoomResponse])
def get_rooms(
    db: Session = Depends(get_db)
):
    return db.query(Room).all()
