import os

from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import (
    Student,
    Room,
    Fee,
    Complaint,
    Visitor
)

from .schemas import (
    StudentCreate,
    StudentResponse,
    RoomResponse,
    ComplaintResponse,
    VisitorResponse
)

load_dotenv()

Base.metadata.create_all(bind=engine)

# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="Hostel Management System API",
    version="1.0.0"
)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Hostel Management System API is running"
    }


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/api/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    total_students = db.query(Student).count()

    total_rooms = db.query(Room).count()


    rooms = db.query(Room).all()


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
            (total_occupied / total_capacity) * 100
        )
        if total_capacity
        else 0
    )


    collected = db.query(Fee).filter(
        Fee.status == "Collected"
    ).all()


    pending = db.query(Fee).filter(
        Fee.status == "Pending"
    ).all()


    fees_collected = sum(
        fee.amount
        for fee in collected
    )


    pending_fees = sum(
        fee.amount
        for fee in pending
    )


    total_expected = (
        fees_collected
        + pending_fees
    )


    collection_rate = (
        round(
            (fees_collected / total_expected) * 100
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


# =========================================================
# STUDENTS
# =========================================================

@app.get(
    "/api/students",
    response_model=list[StudentResponse]
)
def get_students(
    db: Session = Depends(get_db)
):

    return db.query(Student).all()


# =========================================================
# ADD STUDENT
# =========================================================

@app.post(
    "/api/students",
    response_model=StudentResponse
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    existing_student = db.query(Student).filter(
        Student.register == student.register
    ).first()


    if existing_student:

        raise HTTPException(
            status_code=400,
            detail="Register number already exists"
        )


    room = db.query(Room).filter(
        Room.room == student.room
    ).first()


    if not room:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )


    if room.occupied >= room.capacity:

        raise HTTPException(
            status_code=400,
            detail="Room is full"
        )


    new_student = Student(
        name=student.name,
        register=student.register,
        department=student.department,
        year=student.year,
        room=student.room,
        phone=student.phone
    )


    db.add(new_student)


    room.occupied += 1


    db.commit()

    db.refresh(new_student)


    return new_student


# =========================================================
# ROOMS
# =========================================================

@app.get(
    "/api/rooms",
    response_model=list[RoomResponse]
)
def get_rooms(
    db: Session = Depends(get_db)
):

    return db.query(Room).all()


# =========================================================
# FEES
# =========================================================

@app.get("/api/fees")
def get_fees(
    db: Session = Depends(get_db)
):

    fees = db.query(Fee).all()


    collected = sum(
        fee.amount
        for fee in fees
        if fee.status == "Collected"
    )


    pending = sum(
        fee.amount
        for fee in fees
        if fee.status == "Pending"
    )


    total_expected = (
        collected + pending
    )


    collection_rate = (
        round(
            (collected / total_expected) * 100
        )
        if total_expected
        else 0
    )


    return {

        "fees_collected": collected,

        "pending_fees": pending,

        "total_expected": total_expected,

        "collection_rate": collection_rate
    }


# =========================================================
# COMPLAINTS
# =========================================================

@app.get(
    "/api/complaints",
    response_model=list[ComplaintResponse]
)
def get_complaints(
    db: Session = Depends(get_db)
):

    return db.query(Complaint).all()


# =========================================================
# VISITORS
# =========================================================

@app.get(
    "/api/visitors",
    response_model=list[VisitorResponse]
)
def get_visitors(
    db: Session = Depends(get_db)
):

    return db.query(Visitor).all()
