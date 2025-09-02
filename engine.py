from scheduler import create_talent_objects, create_shift_specification, shift_requirements, load_talents, db
from generate import generate_schedule
from datetime import datetime, timedelta

def schedule_talents(start_date, end_date):
    # create talent objects
    talents = load_talents(db)
    talent_objects = create_talent_objects(talents)

    # create shift objects
    shifts = shift_requirements(start_date, end_date)
    shift_objects = create_shift_specification(shifts)

    return generate_schedule(shift_objects, talent_objects)

start_date = datetime.now()
end_date = start_date + timedelta(days=6)

schedule = schedule_talents(start_date, end_date)

print(schedule)