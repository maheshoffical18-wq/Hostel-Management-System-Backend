# backend/app/routers/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Student, Room, Fee, Complaint, Visitor


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    db: Session = Depends(get_db)
):

    total_students = (
        db.query(Student).count()
    )

    rooms = db.query(Room).all()

    total_rooms = len(rooms)

    full_rooms = sum(
        1
        for room in rooms
        if room.occupied >= room.capacity
    )

    available_rooms = sum(
        1
        for room in rooms
        if room.occupied < room.capacity
    )

    total_capacity = sum(
        room.capacity
        for room in rooms
    )

    total_occupied = sum(
        room.occupied
        for room in rooms
    )

    occupancy_percentage = (
        round(
            total_occupied /
            total_capacity * 100
        )
        if total_capacity
        else 0
    )

    fees = db.query(Fee).all()

    fees_collected = sum(
        fee.amount
        for fee in fees
        if fee.status == "Paid"
    )

    pending_fees = sum(
        fee.amount
        for fee in fees
        if fee.status == "Pending"
    )

    total_expected = (
        fees_collected +
        pending_fees
    )

    collection_rate = (
        round(
            fees_collected /
            total_expected * 100
        )
        if total_expected
        else 0
    )

    return {
        "total_students": total_students,
        "total_rooms": total_rooms,
        "full_rooms": full_rooms,
        "available_rooms": available_rooms,

        "total_capacity": total_capacity,
        "total_occupied": total_occupied,
        "occupancy_percentage": occupancy_percentage,

        "fees_collected": fees_collected,
        "pending_fees": pending_fees,
        "total_expected": total_expected,
        "collection_rate": collection_rate
    }
