from datetime import datetime, timedelta
import pandas as pd
from .utils import generate_random_string

import requests

def excell_generate_coins(data):
    inserting_data = {"Номер заявки": [], "Клиент": [], 'Филиал': [],'Сумма':[],  'Комментарий': [], 'Дата создания': []}
    for coin in data:
        inserting_data['Номер заявки'].append(coin.id)
        inserting_data['Клиент'].append(coin.user.full_name)
        inserting_data['Филиал'].append(coin.fillial.parentfillial.name)
        inserting_data['Комментарий'].append(coin.description)
        inserting_data['Сумма'].append(str(coin.price))
        create_time = coin.created_at.strftime("%d.%m.%Y %H:%M:%S")
        inserting_data['Дата создания'].append(create_time)
    file_name = f"files/{generate_random_string()} Coins.xlsx"
    df = pd.DataFrame(inserting_data)
        # Generate Excel file
    df.to_excel(file_name, index=False)
    return file_name



def send_file_to_chat(bot_token, chat_id,file_path):
    # Define the inline keyboard
    payload = {
        'chat_id': chat_id,
    }

    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    # Attach the file
    with open(file_path, 'rb') as file:
        files = {'document': file}
        response = requests.post(url, data=payload, files=files)

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        print(f"Error: {response.text}")
        return False






