import dataclasses
from datetime import date, time
import enum

class Role(enum.Enum):
    leader = "leader"
    server = "server"
    bartender = "bartender"
    hostess = "hostess"
    runner = "runner"

@dataclasses
class shiftSpecification:
    date : date
    start: time
    end: time
    role: Role

@dataclasses
class assignment:
    talent_id : int
    shift : shiftSpecification


