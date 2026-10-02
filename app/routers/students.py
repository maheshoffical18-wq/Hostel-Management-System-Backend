# backend/app/routers/students.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Student, Room
from ..schemas import StudentCreate, StudentResponse


router = APIRouter(
    prefix="/api/students",
    tags=["Students"]
)


@router.get("/", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db)
):
    return db.query(Student).all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.post("/", response_model=StudentResponse)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Student)
        .filter(
            Student.register == student_data.register
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Register number already exists"
        )

    room = (
        db.query(Room)
        .filter(Room.room == student_data.room)
        .first()
    )

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

    student = Student(
        name=student_data.name,
        register=student_data.register,
        department=student_data.department,
        year=student_data.year,
        room=student_data.room,
        phone=student_data.phone
    )

    db.add(student)

    room.occupied += 1

    db.commit()
    db.refresh(student)

    return student
