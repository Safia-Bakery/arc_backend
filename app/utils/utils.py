import requests


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



