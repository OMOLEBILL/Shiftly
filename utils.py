from datetime import datetime, date, time

def map_label_to_time(label: str):
    label = label.lower()
    lookup = {
        'am': (time(6,0), time(15,0)),
        'pm': (time(15,0), time(23,30)),
        'lounge': (time(11,0), time(23,59))
    }
    return lookup.get(label, (time(6,0), time(15,0)))

def create_datetime(date, time):
    return datetime.combine(date, time)
