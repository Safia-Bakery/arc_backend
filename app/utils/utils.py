import json
import random
import string
from datetime import datetime
from http.client import HTTPException
from typing import Optional
import pytz
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from app.core.config import settings
from app.crud import it_requests
from app.db.session import SessionLocal
import os


BASE_URL = 'https://api.service.safiabakery.uz/'
timezonetash = pytz.timezone("Asia/Tashkent")
security = HTTPBasic()
def send_simple_text_message(bot_token: str, chat_id: str, message_text: Optional[str] = None, file: Optional[str] = None):
    if file is not None:
        if not os.path.exists(file):
            print("File not found:", file)
            return False

        with open(file, "rb") as f:
            files = {
                "document": (os.path.basename(file), f)
            }

            payload = {
                "chat_id": chat_id
            }

            if message_text is not None:
                payload["caption"] = message_text
                payload["parse_mode"] = "HTML"

            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendDocument",
                data=payload,
                files=files
            )

            return response if response.status_code == 200 else False

    elif message_text is not None:
        # Send only text
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "HTML"
        }

        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json=payload
        )

        print(response.text)
        return response if response.status_code == 200 else False

    return False


def send_inlinekeyboard_text(bot_token, chat_id, message_text):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Yes', 'callback_data': '-1'}],
            [{'text': 'No', 'callback_data': '-2'}],
        ]
    }

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload, )

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def rating_request_telegram(bot_token, chat_id, message_text, url):
    keyboard = {
        "inline_keyboard": [
            [{"text": "Оставить отзыв🌟", "web_app": {"url": url}}],
        ]
    }

    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "reply_markup": keyboard,
        "parse_mode": "Markdown",
    }

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json=payload,
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def generate_random_string(length=10):
    date_time = datetime.now(timezonetash)
    random_string = date_time.strftime("%d.%m.%Y %H.%M.%S")
    return random_string


def generate_random_filename(length=30):
    # Define the characters you want to use in the random filename
    characters = string.ascii_letters + string.digits

    # Generate a random filename of the specified length
    random_filename = "".join(random.choice(characters) for _ in range(length))

    return random_filename


def sendtotelegramchat(chat_id, message_text, inline_keyboard: Optional[dict] = None):
    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML"
    }

    # Include reply_markup only if keyboard is provided
    if inline_keyboard:
        payload['reply_markup'] = json.dumps(inline_keyboard)

    # Send the request to send the inline keyboard message
    response = requests.post(
        url=f"https://api.telegram.org/bot{settings.bottoken}/sendMessage",
        json=payload
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def send_media_group(chat_id):
    url = f"https://api.telegram.org/bot{settings.bottoken}/sendMediaGroup"
    media = [
        {
            "type": "document",
            "media": "attach://анкета_рус"
        },
        {
            "type": "document",
            "media": "attach://анкета_узб",
            "caption": "Анкеты доступны на узбекском и русском языках"
        }
    ]
    files = {
        "анкета_рус": open("Анкета_шаблон_Рус.pdf", "rb"),
        "анкета_узб": open("Анкета_шаблон_Узб.pdf", "rb")
    }
    data = {
        "chat_id": chat_id,
        "media": json.dumps(media)  # Telegram API expects JSON as a string
    }
    response = requests.post(
        url=url,
        data=data,
        files=files
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def send_files(chat_id, file_urls):
    """
    Prepare the media group for the `sendMediaGroup` method.
    """
    media_group = []
    files = {}
    # Get files from the server
    for i, file_url in enumerate(file_urls):
        media_group.append(
            {
                "type": "document",  # Adjust type as needed (e.g., "photo", "video")
                "media": f"attach://{file_url}"
            }
        )
        files[file_url] = open(f"/var/www/arc_backend/{file_url}", 'rb')

    url = f"https://api.telegram.org/bot{settings.bottoken}/sendMediaGroup"
    data = {
        "chat_id": chat_id,
        "media": json.dumps(media_group)  # Telegram API expects JSON as a string
    }
    response = requests.post(
        url=url,
        data=data,
        files=files
    )
    for file_handle in files.values():
        file_handle.close()

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False



def sendtotelegramtopic(chat_id, message_text, thread_id, inline_keyboard: Optional[dict] = None):
    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "message_thread_id": thread_id,
        "text": message_text,
        "parse_mode": "HTML"
    }
    if inline_keyboard:
        payload['reply_markup'] = json.dumps(inline_keyboard)
    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{settings.bottoken}/sendMessage",
        json=payload,
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def edit_topic_message(chat_id,
                       thread_id,
                       message_id,
                       message_text,
                       inline_keyboard: Optional[dict] = None
                       ):
    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": message_text,
        "parse_mode": "HTML"

    }

    if thread_id:
        payload["message_thread_id"] = thread_id
    if inline_keyboard:
        payload["reply_markup"] = json.dumps(inline_keyboard)

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{settings.bottoken}/editMessageText",
        json=payload,
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def edit_topic_reply_markup(chat_id, thread_id, message_id,
                            inline_keyboard: Optional[dict] = None
                            ):
    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "message_thread_id": thread_id,
        "message_id": message_id,
        "parse_mode": "HTML"

    }

    if inline_keyboard:
        payload['reply_markup'] = json.dumps(inline_keyboard)

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{settings.bottoken}/editMessageReplyMarkup",
        json=payload,
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def inlinewebapp(chat_id, message_text, url):
    keyboard = {
        "inline_keyboard": [
            [{"text": "Оставить отзыв🌟", "web_app": {"url": url}}],
        ]
    }

    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "reply_markup": keyboard,
        "parse_mode": "HTML",
    }

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{settings.bottoken}/sendMessage",
        json=payload,
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def confirmation_request(chat_id, message_text):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Подтвердить', 'callback_data': '10'}],
            [{'text': 'Не сделано', 'callback_data': '11'}],
        ]
    }

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f"https://api.telegram.org/bot{settings.bottoken}/sendMessage", json=payload, )

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def delete_from_chat(message_id, topic_id: Optional[int] = None):
    url = f'https://api.telegram.org/bot{settings.bottoken}/deleteMessage'
    payload = {
        'chat_id': settings.IT_SUPERGROUP,
        'message_id': message_id
    }
    if topic_id:
        payload["message_thread_id"] = topic_id

    # Send a POST request to the Telegram API to delete the message
    response = requests.post(url, json=payload)
    response_data = response.json()
    # Check the response status
    if response.status_code == 200:
        return response_data
    else:
        return False


def send_notification(request_id, topic_id, text, finishing_time, file_url):
    url = f'https://api.telegram.org/bot{settings.bottoken}/sendMessage'
    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "Завершить заявку", "callback_data": "complete_request"},
                {"text": "Отменить", "callback_data": "cancel_request"}
            ],
            [{"text": "Посмотреть фото", "url": f"{BASE_URL}{file_url}"}]
        ] if file_url is not None
        else
        [
            [
                {"text": "Завершить заявку", "callback_data": "complete_request"},
                {"text": "Отменить", "callback_data": "cancel_request"}
            ]
        ]
    }
    now = datetime.now(tz=timezonetash)
    if finishing_time is not None:
        remaining_time = finishing_time - now
        late_time = now - finishing_time

        if finishing_time >= now:
            text = f"{text}\n\n" \
                   f"<b> ‼️ Оставщиеся время:</b>  {str(remaining_time).split('.')[0]}"
        else:
            text = f"{text}\n\n" \
                   f"<b> ‼️ Просрочен на:</b>  {str(late_time).split('.')[0]}"

    payload = {
        'chat_id': settings.IT_SUPERGROUP,
        'message_thread_id': topic_id,  # Include the thread ID for the specific topic
        'text': text,
        'reply_markup': json.dumps(inline_keyboard),
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        new_message_id = response_data["result"]["message_id"]
        with SessionLocal() as db:
            it_requests.edit_request(db=db, id=request_id, tg_message_id=new_message_id)
        return new_message_id
    else:
        return False


def get_current_user_for_docs(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = settings.docs_username
    correct_password = settings.docs_password
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


class JobScheduler:
    def __init__(self):
        # Configure job store
        jobstores = {
            "default": SQLAlchemyJobStore(url=settings.SCHEDULER_DATABASE_URL)
        }
        self.scheduler = BackgroundScheduler(jobstores=jobstores)
        self.scheduler.start()

    def add_delete_message_job(self, job_id, scheduled_time, message_id, topic_id):
        try:
            self.scheduler.add_job("scheduler_jobs.jobs:delete_from_chat", 'date', run_date=scheduled_time,
                                   args=[message_id, topic_id], id=job_id, replace_existing=True)
        except JobLookupError:
            print(f"'{job_id}' job not found or already has completed !")

    def add_send_message_job(self, job_id, scheduled_time, topic_id, request_text, finishing_time, request_id, request_file):
        try:
            self.scheduler.add_job("scheduler_jobs.jobs:send_notification", 'date', run_date=scheduled_time,
                                   args=[request_id, topic_id, request_text, finishing_time, request_file],
                                   id=job_id, replace_existing=True)
        except JobLookupError:
            print(f"'{job_id}' job not found or already has completed !")

    def remove_job(self, job_id):
        try:
            self.scheduler.remove_job(job_id=job_id)
        except JobLookupError:
            print(f"'{job_id}' job not found or already has completed !")