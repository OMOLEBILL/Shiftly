from database import *
from sqlalchemy.orm import Session
from models import *
from datetime import date,time

def shift_periods():
    session = SessionLocal()

    session.add_all(
        [
        Shift_Period(staffing="low", label="AM", start=time(6,0), end=time(15,0)),
        Shift_Period(staffing="high", label="AM", start=time(6,0), end=time(15,0)),
        Shift_Period(staffing="low", label="PM", start=time(15,0), end=time(23,30)),
        Shift_Period(staffing="high", label="PM", start=time(15,0), end=time(23,30)),
        Shift_Period(staffing="low", label="lounge", start=time(11,0), end=time(21,0)),
        Shift_Period(staffing="high", label="lounge", start=time(11,0), end=time(21,0)),
        Shift_Period(staffing="low", label="lounge", start=time(14,0), end=time(0,0)),
        Shift_Period(staffing="high", label="lounge", start=time(14,0), end=time(0,0))
    ]
    )
    session.commit()


    print("All shift periods added")


def talents():
    session = SessionLocal()

    session.add_all([
            Talent(firstname="John", lastname="Doe", email="johndoe@jon.com", role="leader", contract_type="full-time", is_active=True ),
            Talent(firstname="Jamie", lastname="Don", email="jamiedoe@jon.com", role="leader", contract_type="full-time", is_active=True ),
            Talent(firstname="Derrick", lastname="Don", email="derrickdon@jon.com", role="leader", contract_type="full-time", is_active=True ),
            Talent(firstname="Jane", lastname="Doe", email="janedoe@jon.com", role="server", contract_type="full-time", is_active=True ),
            Talent(firstname="Sally", lastname="Doe", email="sallzdoe@jon.com", role="runner", contract_type="part-time", is_active=True ),
            Talent(firstname="Mark", lastname="Doe", email="markdoe@jon.com", role="hostess", contract_type="full-time", is_active=True ),
            Talent(firstname="Peter", lastname="Doe", email="markdoe@jon.com", role="server", contract_type="full-time", is_active=True ),
            Talent(firstname="Lucy", lastname="Doe", email="markdoe@jon.com", role="runner", contract_type="full-time", is_active=True ),
            Talent(firstname="Mason", lastname="Doe", email="markdoe@jon.com", role="hostess", contract_type="full-time", is_active=True ),
            Talent(firstname="TJ", lastname="Doe", email="markdoe@jon.com", role="server", contract_type="full-time", is_active=True ),
            Talent(firstname="Omwami", lastname="Doe", email="markdoe@jon.com", role="server", contract_type="full-time", is_active=True ),
            Talent(firstname="Okino", lastname="Doe", email="markdoe@jon.com", role="server", contract_type="full-time", is_active=True ),
            Talent(firstname="Shaddie", lastname="Doe", email="markdoe@jon.com", role="server", contract_type="full-time", is_active=True ),
            Talent(firstname="Michael", lastname="Doe", email="markdoe@jon.com", role="server", contract_type="full-time", is_active=True ),
            Talent(firstname="Sophia", lastname="Doe", email="markdoe@jon.com", role="runner", contract_type="full-time", is_active=True ),
            Talent(firstname="Doreen", lastname="Doe", email="markdoe@jon.com", role="server", contract_type="full-time", is_active=True ),
            Talent(firstname="Millie", lastname="Doe", email="markdoe@jon.com", role="hostess", contract_type="full-time", is_active=True ),
            Talent(firstname="Osoro", lastname="Doe", email="markdoe@jon.com", role="server", contract_type="full-time", is_active=True ),
            Talent(firstname="Simon", lastname="Doe", email="markdoe@jon.com", role="runner", contract_type="full-time", is_active=True ),
            Talent(firstname="Jennie", lastname="Doe", email="markdoe@jon.com", role="runner", contract_type="full-time", is_active=True ),
            Talent(firstname="Akinyi", lastname="Doe", email="markdoe@jon.com", role="server", contract_type="full-time", is_active=True )
        ])
    session.commit()
    print("all talents added to the db")

    
def constraints():
    session = SessionLocal()


    session.add_all([
        Talent_Constraint(talent_id=4, constraint_type="Semester", is_active=True),
        Talent_Constraint(talent_id=4, constraint_type="AM", is_active=True),
        Talent_Constraint(talent_id=5, constraint_type="Semester", is_active=True),
        Talent_Constraint(talent_id=7, constraint_type="PM", is_active=True),
        Talent_Constraint(talent_id=10, constraint_type="PM", is_active=True),
        Talent_Constraint(talent_id=12, constraint_type="AM", is_active=True),
        Talent_Constraint(talent_id=6, constraint_type="Semester", is_active=True),


    ])


    session.commit()
    print("all constraints added!")


def available_days():


    session = SessionLocal()

    session.add_all([
        Available_Day(constraint_id=1, day="Monday", shifts="AM"),
        Available_Day(constraint_id=1, day="Tuesday", shifts="AM"),
        Available_Day(constraint_id=3, day="Sunday", shifts="PM"),
        Available_Day(constraint_id=2, day="Wednesday", shifts="AM"),
        Available_Day(constraint_id=5, day="Thursday", shifts="PM"),
        Available_Day(constraint_id=2, day="Monday", shifts="AM"),
        Available_Day(constraint_id=1, day="Sunday", shifts="AM"),
        Available_Day(constraint_id=4, day="Friday", shifts="PM"),
        Available_Day(constraint_id=3, day="Saturday", shifts="AM"),
        Available_Day(constraint_id=3, day="Saturday", shifts="AM"),
        Available_Day(constraint_id=6, day="Sunday", shifts="AM"),
        Available_Day(constraint_id=5, day="Friday", shifts="PM"),
        Available_Day(constraint_id=7, day="Wednesday", shifts="AM"),
        Available_Day(constraint_id=7, day="Monday", shifts="AM"),
    ])

    session.commit()
    print("All available days added!")


def shift_template():
    session = SessionLocal()

    templates = [
        Shift_Template(period_id=1, role="leader", count=1),
        Shift_Template(period_id=1, role="server", count=2),
        Shift_Template(period_id=1, role="runner", count=1),
        Shift_Template(period_id=1, role="hostess", count=1),
        Shift_Template(period_id=1, role="bartender", count=1),
        Shift_Template(period_id=2, role="leader", count=2),
        Shift_Template(period_id=2, role="server", count=3),
        Shift_Template(period_id=2, role="runner", count=2),
        Shift_Template(period_id=2, role="hostess", count=2),
        Shift_Template(period_id=2, role="bartender", count=2),
        Shift_Template(period_id=3, role="leader", count=1),
        Shift_Template(period_id=3, role="server", count=2),
        Shift_Template(period_id=3, role="runner", count=1),
        Shift_Template(period_id=3, role="hostess", count=1),
        Shift_Template(period_id=3, role="bartender", count=2),
        Shift_Template(period_id=4, role="leader", count=2),
        Shift_Template(period_id=4, role="server", count=3),
        Shift_Template(period_id=4, role="runner", count=2),
        Shift_Template(period_id=4, role="hostess", count=2),
        Shift_Template(period_id=4, role="bartender", count=3),
        Shift_Template(period_id=5, role="server", count=1),
        Shift_Template(period_id=6, role="server", count=1),
        Shift_Template(period_id=7, role="leader", count=1),
        Shift_Template(period_id=7, role="server", count=2),
        Shift_Template(period_id=8, role="leader", count=1),
        Shift_Template(period_id=8, role="server", count=3),
    ]

    session.add_all(templates)
    session.commit()


    print("All shift templates added!")



def holidays():
    session = SessionLocal()

    holidays = [
        Requests(talent_id=2, requested_date=date(2025, 8, 27), status="approved"),
        Requests(talent_id=5, requested_date=date(2025, 8, 24), status="approved"),
        Requests(talent_id=1, requested_date=date(2025, 8, 28), status="approved"),
        Requests(talent_id=4, requested_date=date(2025, 8, 26), status="approved"),
        Requests(talent_id=6, requested_date=date(2025, 8, 23), status="approved"),
        Requests(talent_id=7, requested_date=date(2025, 8, 29), status="approved"),
        Requests(talent_id=9, requested_date=date(2025, 8, 31), status="approved"),
        Requests(talent_id=9, requested_date=date(2025, 8, 30), status="approved"),
        ]
    
    session.add_all(holidays)
    session.commit()

    print("all holiday requests approved!")
    

    
    

if __name__ == "__main__":
    shift_template()
    available_days()
    constraints()
    talents()
    shift_periods()
    holidays()
