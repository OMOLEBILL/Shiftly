from dataclasses import dataclass
from datetime import date, datetime
import enum

class Role(enum.Enum):
    leader = "leader"
    server = "server"
    bartender = "bartender"
    hostess = "hostess"
    runner = "runner"

@dataclass
class shiftSpecification:
    date : date
    start: datetime
    end: datetime
    role: Role
    count: int

@dataclass
class assignment:
    talent_id : int
    shift : shiftSpecification

@dataclass
class talentAvailability:
    talent_id: int
    role: Role
    window: dict[date, list[tuple[datetime, datetime]]]
    weeklyhours: float

