from collections import defaultdict
from data_class import shiftSpecification, talentAvailability, assignment
from datetime import time

def candidates_for_shift(shift: shiftSpecification, talents_by_role: dict[str, list[int]], window: dict[int, list[tuple[time, time]]]):
    for talent_id in talents_by_role[shift.role]:
        spans = window.get((talent_id, shift.date), [])
        if any(start <= shift.start and end >= shift.end for start, end in spans):
            yield talent_id


def generate_schedule(assignable: list[shiftSpecification], availability: dict[int, talentAvailability]) -> list[assignment]:
    plan: list[assignment] = []
    hours_worked_so_far : dict[int, float] = defaultdict(float)

    #group talents by role
    talents_by_role: dict[str, list[int]] = defaultdict(list)
    for tid, avail in availability.items():
        talents_by_role[avail.role].append(tid)

    #quick lookup  window
    window = {
        (tid, date): spans
        for tid, avail in availability.items()
        for date, spans in avail.window.items()
    }

    #assign shifts to talents
    for shift in assignable:
        cands = list(candidates_for_shift(shift, talents_by_role, window))
        cands.sort(key=lambda tid: availability[tid].weeklyhours - hours_worked_so_far[tid])
        for talent_id in cands:
            duration = (shift.end - shift.start).total_seconds()/3600
            if duration > availability[talent_id].weeklyhours - hours_worked_so_far[talent_id]:
                continue
            plan.append(assignment(talent_id=talent_id, shift=shift))
            hours_worked_so_far[talent_id] += duration
            break

    return plan