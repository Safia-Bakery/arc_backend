from typing import List, Optional
import pytz
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.routes.depth import get_db, get_current_user
from app.schemas.appointments import CreateAppointment, GetAppointment, UpdateAppointment, GetCalendarAppointment
from app.schemas.users import UserGetJustNames
from app.crud.appointments import add_appoinment, get_appoinments, edit_appointment, get_timeslots, \
    get_calendar_appointments
from app.utils.utils import sendtotelegramchat


appointments_router = APIRouter()
timezonetash = pytz.timezone("Asia/Tashkent")
BASE_URL = 'https://api.service.safiabakery.uz/'


@appointments_router.post("/appointments", response_model=GetAppointment)
async def create_appointment(
        data: CreateAppointment,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    try:
        appointment = add_appoinment(data=data, user_id=request_user.id, db=db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    if appointment is False:
        raise HTTPException(status_code=400, detail="Не осталось место на данный промежуток времени!")

    return appointment


@appointments_router.get("/appointments/my_records", response_model=List[GetAppointment])
async def get_my_appointments(
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    appointments = get_appoinments(db=db, user_id=request_user.id)
    return appointments


@appointments_router.get("/appointments", response_model=Page[GetAppointment])
async def get_appointment_list(
        request_id: Optional[int] = None,
        position_id: Optional[int] = None,
        created_user: Optional[str] = None,
        employee_name: Optional[str] = None,
        branch_id: Optional[int] = None,
        status: Optional[int] = None,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    appointments = get_appoinments(
        db=db,
        request_id=request_id,
        position_id=position_id,
        created_user=created_user,
        employee_name=employee_name,
        branch_id=branch_id,
        status=status
    )
    return paginate(appointments)


@appointments_router.get("/appointments/calendar", response_model=List[GetCalendarAppointment])
async def get_calendar_appointment_list(
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    appointments = get_calendar_appointments(db=db)
    return appointments


@appointments_router.get("/appointments/{id}", response_model=GetAppointment)
async def get_appointment(
        id: Optional[int] = None,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    appointment = get_appoinments(db=db, id=id)
    return appointment


@appointments_router.put("/appointments", response_model=GetAppointment)
async def put_appointment(
        data: UpdateAppointment,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    appointment = edit_appointment(db=db, data=data)

    if appointment.status is not None:
        # logs.create_log(db=db, request_id=appointment.id, status=appointment.status, user_id=request_user.id)
        user_telegram_id = appointment.user.telegram_id if appointment.user else None
        days_of_week = {
            "Monday": "Понедельник",
            "Tuesday": "Вторник",
            "Wednesday": "Среда",
            "Thursday": "Четверг",
            "Friday": "Пятница",
            "Saturday": "Суббота",
            "Sunday": "Воскресенье",
        }
        formatted_date = appointment.time_slot.date().strftime('%A %d.%m.%Y')
        formatted_date = formatted_date.replace(
            appointment.time_slot.date().strftime("%A"),
            days_of_week[appointment.time_slot.date().strftime("%A")]
        )

        appointment_info = f"<b>Информация записи:</b>\n" \
                           f"Филиал: {appointment.branch.name}\n" \
                           f"ФИО: {appointment.employee_name}\n" \
                           f"Должность: {appointment.position.name}\n" \
                           f"Комментарий: {appointment.description if appointment.description is not None else ''}\n" \
                           f"Дата: {formatted_date}\n" \
                           f"Время: {appointment.time_slot.time().strftime('%H:%M')}"
        request_text = ""

        if appointment.status == 1:
            request_text = f"Спасибо! Ваша 📑запись #{appointment.id}s на официальное оформление принята.\n\n" \
                           f"{appointment_info}"

        elif appointment.status == 3:
            request_text = f"Здравствуйте! Ваш сотрудник по записи #{appointment.id}s на официальное оформление успешно оформился.\n\n" \
                           f"{appointment_info}"

        elif appointment.status == 4:
            request_text = f"Спасибо! Ваша запись #{appointment.id}s на официальное оформление отменена.\n" \
                           f"<b>Причина отмены:</b> *** {appointment.deny_reason} ***\n\n" \
                           f"{appointment_info}"

        elif appointment.status == 8:
            request_text = f"Здравствуйте! Ваш сотрудник по записи #{appointment.id}s не прошел официальное оформление.\n" \
                           f"<b>Причина:</b> *** {appointment.deny_reason} ***\n\n" \
                           f"{appointment_info}"

        try:
            sendtotelegramchat(chat_id=user_telegram_id, message_text=request_text)
        except Exception as e:
            print(e)

    return appointment


@appointments_router.get("/appointments/time_slot/")
async def get_time_slots(
        query_date: date,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    time_slots = get_timeslots(db=db, date=query_date)
    return time_slots