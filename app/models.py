from sqlalchemy import Column, Integer, String, Float

from .database import Base


class Student(Base):

    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    register = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    department = Column(
        String,
        nullable=False
    )

    year = Column(
        String,
        nullable=False
    )

    room = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=False
    )


class Room(Base):

    __tablename__ = "rooms"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    room = Column(
        String,
        unique=True,
        nullable=False
    )

    capacity = Column(
        Integer,
        nullable=False
    )

    occupied = Column(
        Integer,
        default=0,
        nullable=False
    )


class Fee(Base):

    __tablename__ = "fees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        nullable=True
    )

    amount = Column(
        Float,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )


class Complaint(Base):

    __tablename__ = "complaints"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student = Column(
        String,
        nullable=False
    )

    issue = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )


class Visitor(Base):

    __tablename__ = "visitors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    student = Column(
        String,
        nullable=False
    )

    date = Column(
        String,
        nullable=False
    )
