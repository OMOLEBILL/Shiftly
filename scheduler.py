from models import *
from sqlalchemy.orm import Session
from sqlalchemy import func, cast
from database import SessionLocal
import pandas as pd
from datetime import timedelta, datetime, date
from pprint import pprint
from data_class import shiftSpecification, talentAvailability, assignment
from utils import map_label_to_time

db = SessionLocal()
def load_talents(db: Session):
    query = db.query(
        Talent.id.label("talent_id"),
        func.concat(Talent.firstname, " ", Talent.lastname).label("name"),
        Talent.role.label("role"),
        Talent.is_active,
        Talent.hours,
        Talent_Constraint.constraint_type.label("constraint"),
        Talent_Constraint.is_active.label("active"),
        Available_Day.day,
        Available_Day.shifts,
        Requests.requested_date,
        Requests.status
    ).join(Talent_Constraint, Talent.id == Talent_Constraint.talent_id, isouter=True).join(
        Available_Day, Talent_Constraint.id == Available_Day.constraint_id, isouter=True).join(
            Requests, Talent.id == Requests.talent_id, isouter=True)
    df = pd.read_sql(query.statement, db.bind)
    #print(df)
    return df

def talent_availability(start_date, end_date):
    talents = load_talents(db)
    #define date range
    week = pd.date_range(start_date, end_date)
    #we need date_map because the constraints in the database are day-specific not date specific and we need to map the day to the specific date
    date_map = {day.strftime("%A"): day for day in week}
    #handle talents with constraints, later come and ensure that the dates that go into the dfs are within the defined range we are working with.
    constrained = talents.loc[(talents['constraint'].notna())].groupby(['talent_id', 'day']).agg({'shifts': lambda x: list(set(x)), 'role': 'first'}).reset_index().copy()
    constrained.loc[:,'date'] = constrained['day'].map(date_map).dt.date
    constrained = constrained[['talent_id', 'role', 'date', 'shifts']]
    constrained = constrained.groupby('talent_id').agg({'talent_id': 'first', 'role': 'first', 'date': list, 'shifts': 'first'})
    #handle requests
    requests = talents.loc[(talents['req_date'].notna()) & (talents['status'] == 'approved')].groupby('talent_id')['req_date'].apply(lambda req: set(req)).reset_index()
    requests = requests.set_index('talent_id')['req_date'].to_dict()
    #handle all the talents who do not have any constraints
    shifts = ['AM', 'PM', 'lounge']
    unconstrained = talents.loc[(talents['constraint'].isna())].copy()
    unconstrained.loc[:, 'date']= [list(week)] * len(unconstrained)
    unconstrained['date'] = unconstrained['date'].apply(lambda lst: [d.date() for d in lst])
    unconstrained = unconstrained[['talent_id', 'role', 'date']]
    unconstrained.loc[:, 'shifts'] = [shifts] * len(unconstrained)
    unconstrained = unconstrained.drop_duplicates(subset=['talent_id'])
    all_talents = pd.concat([constrained, unconstrained], ignore_index=True).copy()

    #remove all the requested dates for every talent.
    for tid, dates in all_talents[['talent_id', 'date']].itertuples(index=None, name=None):
        req_dates = requests.get(tid, set())
        filtered = [d for d in dates if d not in req_dates]
        idx = all_talents.index[all_talents['talent_id'] == tid][0]
        if not filtered: #if there is a talent who does not have any shifts at all, drop them from the list completely
            all_talents = all_talents.drop(idx)
        else:
            all_talents.at[idx, 'date'] = filtered

    pprint(all_talents)
    return all_talents


def create_talent_objects(talents: pd.DataFrame, weeklyhours: float = 32) -> dict[int, talentAvailability]:
    """
    Returns a list of talent objects from the talent dataframes

    Args:
        talents: dataframe with all available talents
    Return:
        list: talentAvailability
    """
    talent_list = talents.to_dict('records')
    talent_object: dict[int, talentAvailability] = {}
    for talent in talent_list:
        for date in list(talent.get('date', [])):
            window: dict = {}
            window[date] = []
            for shift in list(talent.get('shifts', [])):
                shift_span = map_label_to_time(date, shift)
                window[date].append(shift_span)
            talent_object[talent.get('talent_id')] = talentAvailability(
                talent_id=talent.get('talent_id'),
                role=talent.get('role'),
                window=window,
                weeklyhours=weeklyhours
            )
    return talent_object

def create_shift_specification(shift_requirements: pd.DataFrame) -> list[shiftSpecification]:
    """
    Returns a list of objects from the shift_requirements dataframes

    Args:
        shift_requirements : dataframe of all shifts that need to be populated

    Return:
        list: shiftSpecification
    """
    shift_list = shift_requirements.to_dict('records')
    shift_specification_object = []
    for shift in shift_list:
        shift.pop('day'); shift.pop('staffing'); shift.pop('shift')
        shift_specification_object.append(shiftSpecification(**shift))

    return shift_specification_object


def load_shift_periods(db: Session):
    query = db.query(
        Shift_Period.id.label('period_id'),
        cast(Shift_Period.staffing, String).label("staffing"),
        Shift_Period.label.label('shift'),
        Shift_Period.start,
        Shift_Period.end,
        cast(Shift_Template.role, String).label('role'),
        Shift_Template.count
    ).join(Shift_Template, Shift_Period.id == Shift_Template.period_id, isouter=True)

    df = pd.read_sql(query.statement, db.bind)
    return df

def shift_requirements(start_date, end_date, database = db):
    templates = load_shift_periods(database)
    week = pd.date_range(start_date, end_date)
    #here I built the dataframe from scratch then merged it with the existing templates based on matching staffing requirements
    week_df = pd.DataFrame({'date': [day.date() for day in week]})
    week_df.loc[:, 'day'] = [day.strftime("%A") for day in week]
    week_df.loc[:, 'staffing'] = week_df['day'].apply(lambda day: staffing.low.value if day in staffing_days[staffing.low] else staffing.high.value)
    week_shifts = week_df.merge(templates[['staffing', 'shift', 'start', 'end', 'role', 'count']],on='staffing',how='left')
    return week_shifts


# use classes instead so that it is easier to scale
# separate talent availability and shift_requirements
def schedule_talents(start_date, end_date):
    pass
def hours_completed():
    #this is a helper function to compute the number of hours a talent has been scheduled for.
    pass

def morning_allowance():
    #this is a helper function to ensure that at least 1/3 of the shifts worked by a talent in a month are morning shifts
    pass

def is_eligible():
    #this is a function to check the hard constraints that have to be enforced in order for a talent to be scheduled for a shift.
    #This function is going to return true or false
    #The constraints here are:
    # 1. A talent cannot work for more than 6 days straight
    # 2. There must be at least 11 hours between a talent's two shifts
    # 4. A talent cannot work for more than the hours on their contract (it can go up by 2-4 hours )
    pass





#this is test data to check if the code is working
today = datetime.now()
week = today + timedelta(days=6)

#load_shift_periods(db)
#load_talents(db)
#talent= talent_availability(today, week)
#objects = create_talent_objects(talent)
#pprint(objects)

data = shift_requirements(today, week)
objects = create_shift_specification(data)
print(objects)
#pprint(data.to_dict('records'))
#schedule_talents(today, week)


# create classes for rules to be followed



