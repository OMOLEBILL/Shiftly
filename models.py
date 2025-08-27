from database import Base
from sqlalchemy import Enum as PyEnum, Column, Integer, String, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum


class staffing(enum.Enum):
    low = "low"
    high = "high"

staffing_days = {
    staffing.low: ["Monday", "Tuesday", "Wednesday", "Thursday"],
    staffing.high: ["Friday", "Saturday", "Sunday"]
}



class Talent(Base):
    __tablename__ = "talents"

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    email = Column("email", String, nullable=True)
    role = Column("role", String, nullable=False)
    contract_type = Column("contract_type", String, nullable=False, default="full-time")
    is_active = Column("is_active", Boolean, default=True)
    hours = Column("hours", Integer)
    start_date = Column("start_date", Date)
    end_date = Column("end_date", Date)
    constraints = relationship("Talent_Constraint", back_populates="talent")
    requests = relationship("Requests", back_populates="talent")

    def __init__(self, **kwargs):
       super().__init__(**kwargs)
       contract_hours = {
           'fulltime':40, 
           'partime':30
       }
       self.hours = contract_hours.get(self.contract_type, 24)
       


class Talent_Constraint(Base):
    __tablename__ = "talent_constraints"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    talent_id = Column(Integer, ForeignKey('talents.id'))
    constraint_type = Column("type", String)
    is_active = Column("is_active", Boolean, default=False)
    talent = relationship("Talent", back_populates="constraints")
    available_days = relationship("Available_Day", back_populates="constraints", cascade="all, delete-orphan")



class Available_Day(Base):
    __tablename__ = 'available_days'

    id = Column("id", Integer, primary_key= True, autoincrement=True)
    constraint_id = Column(Integer, ForeignKey("talent_constraints.id"))
    day = Column("day", String)
    shifts = Column("shifts", String) #either all day, AM, or PM
    constraints = relationship("Talent_Constraint", back_populates="available_days")



class Requests(Base):
    __tablename__ = "requests"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    talent_id = Column(Integer, ForeignKey("talents.id"))
    requested_date = Column("req_date", Date)
    status = Column("status", String, default="pending")
    created_at = Column("created", Date, default=datetime.now(timezone.utc))
    updated_at = Column("updated_at", Date, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    talent = relationship("Talent", back_populates="requests")

    

class Scheduled_Shift(Base):
    __tablename__ = "scheduled_shifts"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    talent_id = Column(Integer, ForeignKey("talents.id"))
    date_of = Column("date", Date)
    start_time = Column("start_time", Time)
    end_time = Column("end_time", Time)
    is_locked = Column("is_locked", Boolean, default=False)
    total_hours = Column("total_hours", Integer)



class Weekly_Schedule(Base):
    __tablename__ = "weekly_schedules"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    week_start = Column("week_start", Date)
    generate_by = Column("generated_by", String)
    created_at =Column("created_at", Date, default=datetime.now(timezone.utc))
    is_finalized = Column("finalized", Boolean, default=False)
   


class Shift_Period(Base):
    __tablename__ = "shift_period"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    staffing = Column("staffing", PyEnum(staffing))
    label = Column("shift", String, nullable=False) #AM, PM, Lounge
    start = Column("start", Time)
    end = Column("end", Time)
    templates = relationship("Shift_Template", back_populates="period")



class Shift_Template(Base):

    __tablename__ = "shift_templates"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    period_id = Column(Integer, ForeignKey("shift_period.id"))
    role = Column("role", String, nullable=False)
    count = Column("count", Integer, default=1)
    period = relationship("Shift_Period", back_populates="templates")

        

class Event(Base):

    __tablename__ = "events"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    shift_id = Column(Integer, ForeignKey("scheduled_shifts.id"))
    name = Column("event_name", String)
    date = Column("date", Date)
    is_mandatory = Column("mandatory", Boolean) #this means that all talents have to attend
    start_time = Column("start_time", Time)
    end_time = Column("end_time", Time)
    status = Column("status", String, default="confirmed") # this is in case the event is posptponed to a later date or cancelled altogether
    created_at = Column("created_at", Date, default=datetime.now(timezone.utc))
    updated_at = Column("updated_at", Date, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
