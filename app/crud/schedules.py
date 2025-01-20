from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.appointments import Appointments
from app.schemas.schedules import CreateSchedule, UpdateSchedule

from app.models.schedules import Schedule


def get_all_actual_schedules(db: Session):
    current_date = datetime.now().date()
    actual_schedules = db.query(Schedule).filter(
        Schedule.date >= current_date
    ).all()
    return actual_schedules


def get_one_schedule(db: Session, id):
    schedule = db.query(Schedule).get(ident=id)
    return schedule


def add_schedule(db: Session, data: CreateSchedule):
    appointments = db.query(Appointments).filter(
        and_(
            func.date(Appointments.time_slot) == data.date,
            Appointments.status != 4
        )
    ).all()
    if not appointments:
        schedule = Schedule(
            date=data.date,
            time=data.time,
            is_available=data.is_available,
            description=data.description
        )
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule
    else:
        return None


def edit_schedule(db: Session, data: UpdateSchedule):
    schedule = db.query(Schedule).get(ident=data.id)
    if data.time is not None:
        schedule.time = data.time
    if data.is_available is not None:
        schedule.is_available = data.is_available
    if data.description is not None:
        schedule.description = data.description

    db.commit()
    db.refresh(schedule)
    return schedule


def delete_schedule(db: Session, id):
    schedule = db.query(Schedule).get(ident=id)
    db.delete(schedule)
    db.commit()
    return None
