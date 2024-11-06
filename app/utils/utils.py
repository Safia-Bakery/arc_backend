import json
from typing import Optional

import requests
import string
import random
from app.core.config import settings
from datetime import datetime
import pytz

from app.crud import it_requests

timezonetash = pytz.timezone("Asia/Tashkent")


def send_simple_text_message(bot_token, chat_id, message_text):
    # Create the request payload
    payload = {"chat_id": chat_id, "text": message_text, "parse_mode": "HTML"}

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
    random_string = date_time.strftime("%Y-%m-%d%H:%M:sd%S")
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
        # "reply_markup": json.dumps(inline_keyboard) or None,
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


def sendtotelegramtopic(chat_id, message_text, thread_id):
    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "message_thread_id": thread_id,
        "text": message_text,
        "parse_mode": "HTML"
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


def edit_topic_message(chat_id,
                       thread_id,
                       message_id,
                       message_text,
                       inline_keyboard: Optional[dict] = None
                       ):
    # Create the request payload
    payload = {
        "chat_id": chat_id,
        # "message_thread_id": thread_id,
        "message_id": message_id,
        "text": message_text,
        # "reply_markup": json.dumps(inline_keyboard),
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
    print(response.json())
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
        # "reply_markup": json.dumps(inline_keyboard),
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
    base_url = f'https://api.telegram.org/bot{settings.bottoken}'
    delete_url = f"{base_url}/deleteMessage"
    delete_payload = {
        'chat_id': settings.IT_SUPERGROUP,
        'message_id': message_id
    }
    if topic_id:
        delete_payload["message_thread_id"] = topic_id

    # Send a POST request to the Telegram API to delete the message
    response = requests.post(delete_url, data=delete_payload)
    response_data = response.json()
    # Check the response status
    if response.status_code == 200:
        return response_data
    else:
        return False


def send_notification(db, request_id, message_id, topic_id, text):
    base_url = f'https://api.telegram.org/bot{settings.bottoken}'

    inline_keyboard = {
        "inline_keyboard": [
            [{"text": "Завершить заявку", "callback_data": "complete_request"},
             {"text": "Отправить сообщение заказчику", "callback_data": "send_message_to_user"}]
        ]
    }

    send_url = f"{base_url}/sendMessage"
    send_payload = {
        'chat_id': settings.IT_SUPERGROUP,
        'message_id': message_id,
        'message_thread_id': topic_id,  # Include the thread ID for the specific topic
        'text': text,
        'reply_markup': json.dumps(inline_keyboard),
        'parse_mode': 'HTML'
    }
    response = requests.post(send_url, json=send_payload)
    if response.status_code == 200:
        response_data = response.json()
        new_message_id = response_data["result"]["message_id"]
        it_requests.edit_request(db=db, id=request_id, tg_message_id=new_message_id)
    else:
        return False

