from database import Base, engine, SessionLocal
from models import Student, Room, Fee, Complaint, Visitor

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Prevent duplicate seed data
# if db.query(Student).count() == 0:

#     students = [
#         Student(
#             name="Maheshwaran S",
#             register="C4S22184",
#             department="BCA",
#             year="3rd Year",
#             room="18",
#             phone="7708043539"
#         ),
#         Student(
#             name="Arun Kumar",
#             register="C4S22101",
#             department="BCA",
#             year="2nd Year",
#             room="12",
#             phone="9876543210"
#         ),
#         Student(
#             name="Priya S",
#             register="C4S22115",
#             department="BSc CS",
#             year="3rd Year",
#             room="21",
#             phone="9876501234"
#         ),
#         Student(
#             name="Karthik R",
#             register="C4S22120",
#             department="BCA",
#             year="1st Year",
#             room="15",
#             phone="9123456789"
#         ),
#         Student(
#             name="Divya M",
#             register="C4S22125",
#             department="BCom",
#             year="2nd Year",
#             room="10",
#             phone="9000001234"
#         ),
#         Student(
#             name="Sanjay P",
#             register="C4S22130",
#             department="BCA",
#             year="3rd Year",
#             room="25",
#             phone="9888888888"
#         ),
#     ]

#     db.add_all(students)


if db.query(Room).count() == 0:

    rooms = [
        Room(room="10", capacity=4, occupied=2),
        Room(room="12", capacity=4, occupied=3),
        Room(room="15", capacity=4, occupied=2),
        Room(room="18", capacity=4, occupied=4),
        Room(room="21", capacity=4, occupied=3),
        Room(room="25", capacity=4, occupied=2),
    ]

    db.add_all(rooms)


if db.query(Fee).count() == 0:

    fees = [
        Fee(
            amount=145000,
            status="Collected"
        ),
        Fee(
            amount=80000,
            status="Pending"
        ),
    ]

    db.add_all(fees)


if db.query(Complaint).count() == 0:

    complaints = [
        Complaint(
            student="Arun Kumar",
            issue="Fan not working",
            status="Pending"
        ),
        Complaint(
            student="Priya S",
            issue="Water problem",
            status="Resolved"
        ),
    ]

    db.add_all(complaints)


if db.query(Visitor).count() == 0:

    visitors = [
        Visitor(
            name="Parent - Maheshwaran",
            student="Maheshwaran S",
            date="29-09-2026"
        ),
        Visitor(
            name="Parent - Arun",
            student="Arun Kumar",
            date="29-09-2026"
        ),
    ]

    db.add_all(visitors)


db.commit()
db.close()

print("Database seeded successfully.")
