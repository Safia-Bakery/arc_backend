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


