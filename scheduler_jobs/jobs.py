import json
from typing import Optional
import pytz
import requests
from app.core.config import settings
from datetime import datetime
from app.crud import it_requests
from app.db.session import SessionLocal


timezonetash = pytz.timezone("Asia/Tashkent")
BASE_URL = "https://api.service.safiabakery.uz/"


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
    else:
        return False
