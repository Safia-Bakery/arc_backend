from datetime import datetime, timedelta
from typing import Optional
import pytz
from sqlalchemy import func, cast, Date, Time, and_
from sqlalchemy.orm import Session
from app.schemas.appointments import CreateAppointment, UpdateAppointment
from app.models.appointments import Appointments
from app.models.users_model import Users


timezonetash = pytz.timezone("Asia/Tashkent")


def add_appoinment(data: CreateAppointment, user_id, db: Session):
    appointments = db.query(Appointments).filter(
        and_(
            Appointments.time_slot == data.time_slot,
            Appointments.status != 4
        )
    ).all()
    if len(appointments) < 2:
        obj = Appointments(
            employee_name=data.employee_name,
            time_slot=data.time_slot,
            description=data.description,
            department=12,
            position_id=data.position_id,
            user_id=user_id,
            branch_id=data.branch_id
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    return False


def get_appoinments(
        db: Session,
        request_id: Optional[int] = None,
        position_id: Optional[int] = None,
        created_user: Optional[str] = None,
        employee_name: Optional[str] = None,
        branch_id: Optional[int] = None,
        status: Optional[int] = None,
        user_id: Optional[int] = None,
        id: Optional[int] = None
):
    obj = db.query(Appointments)
    if request_id is not None:
        obj = obj.filter(Appointments.id == request_id)
    if position_id is not None:
        obj = obj.filter(Appointments.position_id == position_id)
    if created_user is not None:
        obj = obj.join(Users).filter(Users.full_name.ilike(f"%{created_user}%"))
    if employee_name is not None:
        obj = obj.filter(Appointments.employee_name.ilike(f"%{employee_name}%"))
    if branch_id is not None:
        obj = obj.filter(Appointments.branch_id == branch_id)
    if status is not None:
        obj = obj.filter(Appointments.status == status)
    if user_id is not None:
        obj = obj.filter(Appointments.user_id == user_id)
    if id is not None:
        obj = obj.get(ident=id)
        return obj

    return obj.order_by(Appointments.id.desc()).all()


def get_calendar_appointments(db: Session):
    now = datetime.now().date()
    from_date = now - timedelta(days=14)
    to_date = now + timedelta(days=14)
    obj = db.query(Appointments).filter(
        and_(
            func.date(Appointments.time_slot).between(from_date, to_date),
            Appointments.status != 4
        )
    )

    return obj.order_by(Appointments.id.desc()).all()


def edit_appointment(db: Session, data: UpdateAppointment):
    obj = db.query(Appointments).get(ident=data.id)
    if data.employee_name is not None:
        obj.employee_name = data.employee_name
    if data.status is not None:
        obj.status = data.status
        # updated_data = obj.update_time or {}
        # updated_data[str(data.status)] = str(now)
        # if data.status == 1:
        #     obj.started_at = now
        # elif data.status in [3, 4, 6, 8]:
        #     obj.finished_at = now
        #
        # db.query(Requests).filter(Requests.id == obj.id).update({"update_time": updated_data})

    if data.description is not None:
        obj.description = data.description
    if data.deny_reason is not None:
        obj.deny_reason = data.deny_reason

    db.commit()
    db.refresh(obj)
    return obj


def get_timeslots(db: Session, date):
    obj = db.query(
        # Appointments
        func.cast(Appointments.time_slot, Time).label("time"),
        func.count(Appointments.id).label('count')
    ).filter(
        and_(
            func.date(Appointments.time_slot) == date,
            Appointments.status != 4
        )
    ).group_by(
        func.cast(Appointments.time_slot, Time)
    ).order_by(
        func.cast(Appointments.time_slot, Time)
    ).all()
    all_slots = ["09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "14:30", "15:00", "15:30",
                 "16:00", "16:30"]
    all_slots_copy = all_slots.copy()
    reserved = {}
    free = {}
    for row in obj:
        objs = db.query(Appointments).filter(
            and_(
                func.date(Appointments.time_slot) == date,
                func.cast(Appointments.time_slot, Time) == row.time,
                Appointments.status != 4
            )
        ).all()
        if row.count < 2 and len(objs) < 2:
            free[row.time.strftime("%H:%M")] = objs
        else:
            reserved[row.time.strftime("%H:%M")] = objs

    for item in reserved.keys():
        if item in all_slots_copy:
            all_slots_copy.remove(item)

    for item in all_slots_copy:
        if item not in free.keys():
            free[item] = []

    return {"all": all_slots, "reserved": reserved, "free": free}
