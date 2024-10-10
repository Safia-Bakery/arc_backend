from datetime import datetime, timedelta
import pandas as pd


def name_generator(length=20):
    import random
    import string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


statusdata = {'0':'Новый','1':'Принят',"2":'Принят','3':'Закончен','4':'Закрыт,отменен','5':'Остановлен','6':"Решен","7":'Принят','8':'Отменен'}


def excell_generate_it(data):
    inserting_data = {"Номер заявки": [], "Клиент": [], "Исполнитель": [], 'Филиал': [], 'Дата создания': [],
                      'Дата окончания': [], 'Дедлайн': [], 'Статус': [], 'Категория': [], 'Комментарий': [],
                      "Срочно": [], 'Дата решения': [], 'Дата отмены': [], 'Переоткрыта': []}
    for row in data:
        inserting_data['Номер заявки'].append(row.id)
        inserting_data['Клиент'].append(row.user.full_name)

        inserting_data['Филиал'].append(row.fillial.parentfillial.name)
        inserting_data['Категория'].append(row.category.name)
        inserting_data['Комментарий'].append(row.description)
        inserting_data['Статус'].append(statusdata[str(row.status)])

        create_time = row.created_at.strftime("%d.%m.%Y %H:%M:%S")
        inserting_data['Дата создания'].append(create_time)
        if row.finishing_time:
            deadline = row.finishing_time.strftime("%d.%m.%Y %H:%M:%S")
        else:
            deadline = ""
        if row.brigada_id is not None:
            inserting_data['Исполнитель'].append(row.brigada.name)
        else:
            inserting_data['Исполнитель'].append('')

        if row.category.urgent:
            inserting_data['Срочно'].append("Да")
        else:
            inserting_data['Срочно'].append("Нет")

        inserting_data['Дедлайн'].append(deadline)

        if row.update_time:
            reshen_time = dict(row.update_time).get('6')
            if reshen_time:
                reshen_time = datetime.strptime(reshen_time, "%Y-%m-%d %H:%M:%S.%f%z")

                # Now you can use the strftime method
                reshen_time = reshen_time.strftime("%d.%m.%Y %H:%M:%S")

                inserting_data['Дата решения'].append(reshen_time)
            else:
                inserting_data['Дата решения'].append("")
            # delayed = dict(row.update_time).get('5')
            # if delayed:
            # delayed = datetime.strptime(delayed, "%Y-%m-%d %H:%M:%S.%f%z")
            #
            #    Now you can use the strftime method
            # delayed = delayed.strftime("%d.%m.%Y %H:%M:%S")
            # inserting_data['Дата приостановки'].append(delayed)
            # else:
            # inserting_data['Дата приостановки'].append("")
            finish_time = dict(row.update_time).get('3')
            if finish_time:
                try:
                    finish_time = datetime.strptime(finish_time, "%Y-%m-%d %H:%M:%S.%f%z")
                except:
                    finish_time = datetime.strptime(finish_time, "%Y-%m-%dT%H:%M:%S.%f%z")

                # Now you can use the strftime method
                finish_time = finish_time.strftime("%d.%m.%Y %H:%M:%S")
                inserting_data['Дата окончания'].append(finish_time)
            else:
                inserting_data['Дата окончания'].append("")
            reopened = dict(row.update_time).get('7')
            if reopened:
                inserting_data['Переоткрыта'].append("Да")
            else:
                inserting_data['Переоткрыта'].append("Нет")

        else:
            inserting_data['Дата решения'].append("")
            inserting_data['Дата приостановки'].append("")

        if row.status == 4 or row.status == 8:
            if row.update_time:
                cancel_time = dict(row.update_time).get('4')
                cancel_time8 = dict(row.update_time).get('8')
                if cancel_time8:
                    try:
                        cancel_time8 = datetime.strptime(cancel_time8, "%Y-%m-%d %H:%M:%S.%f%z")
                    except:
                        cancel_time8 = datetime.strptime(cancel_time8, "%Y-%m-%dT%H:%M:%S.%f%z")

                    # Now you can use the strftime method
                    cancel_time = cancel_time8.strftime("%d.%m.%Y %H:%M:%S")
                elif cancel_time:
                    try:
                        cancel_time = datetime.strptime(cancel_time, "%Y-%m-%d %H:%M:%S.%f%z")
                    except:
                        cancel_time = datetime.strptime(cancel_time, "%Y-%m-%dT%H:%M:%S.%f%z")

                    # Now you can use the strftime method
                    cancel_time = cancel_time.strftime("%d.%m.%Y %H:%M:%S")

                inserting_data['Дата отмены'].append(cancel_time)
            else:
                inserting_data['Дата отмены'].append("")
        else:
            inserting_data['Дата отмены'].append("")

        # if row.finished_at:
        #    if row.status !=3:
        #        inserting_data['Переоткрыта'].append("Да")
        #    else:
        #        inserting_data['Переоткрыта'].append("Нет")
        # else:
        #    inserting_data['Переоткрыта'].append("Нет")

    file_name = f"files/{name_generator()}.xlsx"
    df = pd.DataFrame(inserting_data)
    # Generate Excel file
    df.to_excel(file_name, index=False)
    return file_name


def uniform_excell_generate(data):
    inserting_data = {"Номер заявки":[],"Филиал":[],'Дата поступления':[],"Форма":[],'Общ. сумма':[],'Сотрудник':[],'Статус':[]}
    for row in data:
        forma_list = ''
        total_sum = 0
        inserting_data['Номер заявки'].append(row.id)
        inserting_data['Филиал'].append(row.fillial.parentfillial.name)
        for product in row.request_orpr:
            forma_list += f"{product.orpr_product.prod_cat.name} {product.orpr_product.name} x {product.amount}\n"
            if product.orpr_product.prod_cat.price:
                total_sum += product.orpr_product.prod_cat.price*product.amount
        inserting_data['Форма'].append(forma_list)
        inserting_data['Сотрудник'].append(row.description)
        inserting_data['Статус'].append(statusdata[str(row.status)])
        create_time = (row.created_at+timedelta(hours=5)).strftime("%d.%m.%Y %H:%M:%S")
        inserting_data['Дата поступления'].append(create_time)
        inserting_data['Общ. сумма'].append(total_sum)

    file_name = f"files/{name_generator()}.xlsx"
    df = pd.DataFrame(inserting_data)
    # Generate Excel file
    df.to_excel(file_name, index=False)

    return file_name
