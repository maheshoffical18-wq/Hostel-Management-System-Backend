from pydantic import BaseModel


class StudentCreate(BaseModel):

    name: str
    register: str
    department: str
    year: str
    room: str
    phone: str


class StudentResponse(StudentCreate):

    id: int

    class Config:
        from_attributes = True


class RoomResponse(BaseModel):

    id: int
    room: str
    capacity: int
    occupied: int

    class Config:
        from_attributes = True


class ComplaintResponse(BaseModel):

    id: int
    student: str
    issue: str
    status: str

    class Config:
        from_attributes = True


class VisitorResponse(BaseModel):

    id: int
    name: str
    student: str
    date: str

    class Config:
        from_attributes = True
