from datetime import datetime, date, time

def map_label_to_time(date: date, label: str):
    label = label.lower()
    lookup = {
        'am': (create_datetime(date, time(6,0)), create_datetime(date, time(15,0))),
        'pm': (create_datetime(date, time(15,0)), create_datetime(date, time(23,30))),
        'lounge': (create_datetime(date, time(11,0)), create_datetime(date, time(23,59)))
    }
    return lookup.get(label, (create_datetime(date, time(6,0)), create_datetime(date, time(15,0))))

def create_datetime(date, time):
    return datetime.combine(date, time)