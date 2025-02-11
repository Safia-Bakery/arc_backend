from datetime import timedelta
import pandas as pd
from sqlalchemy import and_, func, distinct
from sqlalchemy.orm import Session
from app.models.kru_finished_tasks import KruFinishedTasks
from app.models.kru_tasks import KruTasks
from app.models.kru_categories import KruCategories
from app.models.tools import Tools
from app.models.parentfillials import ParentFillials
from app.models.tool_branch_relations import ToolBranchCategoryRelation
from app.schemas.kru_reports import KruReport
from microservices import name_generator, generate_random_string_datetime
from app.db.session import SessionLocal


def get_all_tasks(category_id):
    with SessionLocal() as session:
        tasks = session.query(
            KruTasks
        ).filter(
            KruTasks.kru_category_id == category_id
        ).order_by(
            KruTasks.id
        ).all()

    return tasks


def get_branch_results(branch_id, query_date):
    with SessionLocal() as session:
        branch_tools = session.query(
            func.count(ToolBranchCategoryRelation.tool_id)
        ).filter(
            ToolBranchCategoryRelation.branch_id == branch_id
        ).scalar()
        finished_tools = session.query(
            func.count(distinct(KruFinishedTasks.tool_id))
        ).filter(
            and_(
                KruFinishedTasks.branch_id == branch_id,
                func.date(KruFinishedTasks.created_at) == query_date
            )
        ).scalar()

    if branch_tools == 0:
        result = 0
    else:
        result = (finished_tools / branch_tools)

    result = result * 100

    return result


def get_all_branches_for_category():
    with SessionLocal() as session:
        branches = session.query(
            ParentFillials
        ).join(
            KruFinishedTasks, KruFinishedTasks.branch_id == ParentFillials.id
        ).all()

    return branches


def get_max_date_of_finished_tasks():
    with SessionLocal() as session:
        max_date = session.query(
            func.max(func.date(KruFinishedTasks.created_at))
        ).scalar()

    return max_date


def get_kru_report(db: Session, data: KruReport):
    finish_date = data.finish_date + timedelta(days=1)
    query = db.query(
        KruFinishedTasks
    ).join(
        ParentFillials, KruFinishedTasks.branch_id == ParentFillials.id
    ).join(
        KruTasks, KruFinishedTasks.task_id == KruTasks.id
    ).join(
        KruCategories, KruTasks.kru_category_id == KruCategories.id
    ).join(
        Tools, KruFinishedTasks.tool_id == Tools.id
    ).filter(
        and_(
            func.date(KruFinishedTasks.created_at).between(data.start_date, finish_date),
            KruCategories.id == data.category_id
        )
    )
    # if data.report_type == 1:
    if data.branch_id is not None:
        query = query.filter(KruFinishedTasks.branch_id == data.branch_id)
    if data.product_code is not None:
        query = query.filter(Tools.code == data.product_code)
    if data.product_name is not None:
        query = query.filter(Tools.name == data.product_name)
    if data.answer is not None:
        query = query.filter(KruFinishedTasks.comment == data.answer)


    # return query.order_by(KruFinishedTasks.id.desc()).all()
    query = query.order_by(
        func.date(KruFinishedTasks.created_at),
        KruFinishedTasks.branch_id,
        KruFinishedTasks.tool_id,
        KruFinishedTasks.task_id
    ).all()

    return query



def top50_excell_generator(data, report_type, start_date, finish_date):
    inserting_data = {}
    if report_type == 1:
        inserting_data = {
            "Филиал": [],
            "Артикул": [],
            "Наименование товара": [],
            "Причина": [],
            "Дата": []
        }

        for row in data:
            inserting_data['Филиал'].append(row.branch.name)
            inserting_data['Артикул'].append(row.tool.code) if row.tool else inserting_data['Артикул'].append(" ")
            inserting_data['Наименование товара'].append(row.tool.name) if row.tool else inserting_data['Наименование товара'].append(" ")
            inserting_data['Причина'].append(row.comment)
            inserting_data['Дата'].append(row.created_at.strftime('%Y-%m-%d'))

    elif report_type == 2:
        inserting_data = {
            "Дата": [],
            "Филиал": [],
            "Товар": [],
            "Артикул": []
        }
        tasks = get_all_tasks(category_id=26)
        for task in tasks:
            inserting_data[task.name] = []

        for row in data:
            inserting_data[row.task.name].append(row.comment)
            task_len = len(inserting_data[row.task.name])

            try:
                inserting_data['Дата'][task_len-1] = row.created_at.strftime('%Y-%m-%d')
            except IndexError:
                inserting_data['Дата'].append(row.created_at.strftime('%Y-%m-%d'))

            try:
                inserting_data['Филиал'][task_len-1] = row.branch.name
            except IndexError:
                inserting_data['Филиал'].append(row.branch.name)

            try:
                inserting_data['Товар'][task_len-1] = row.tool.name
            except IndexError:
                inserting_data['Товар'].append(row.tool.name)

            try:
                inserting_data['Артикул'][task_len-1] = row.tool.code
            except IndexError:
                inserting_data['Артикул'].append(row.tool.code)

            # if row.branch.name not in inserting_data['Филиал']:
            #     inserting_data['Филиал'].append(row.branch.name)
            # if row.tool.name not in inserting_data['Товар']:
            #     inserting_data['Товар'].append(row.tool.name)
            # if row.tool.code not in inserting_data['Артикул']:
            #     inserting_data['Артикул'].append(row.tool.code)

            # for task in tasks:
            #     if task.name == row.task.name:
            #         inserting_data[task.name].append(row.comment) if row.comment else inserting_data[task.name].append(" ")

    elif report_type == 3:
        inserting_data = {
            "Филиал": []
        }
        all_branches = get_all_branches_for_category()
        all_branches = [branch for branch in all_branches]
        for branch in all_branches:
            inserting_data["Филиал"].append(branch.name)

        current_date = start_date
        max_date = get_max_date_of_finished_tasks()
        if finish_date > max_date:
            finish_date = max_date
        while current_date <= finish_date:
            result_values = []
            for branch in all_branches:
                result_values.append(get_branch_results(branch_id=branch.id, query_date=current_date))
            inserting_data[str(current_date)] = result_values
            current_date += timedelta(days=1)

    file_name = f"files/top50_{generate_random_string_datetime()}.xlsx"
    df = pd.DataFrame(inserting_data)
    # Generate Excel file
    df.to_excel(file_name, index=False)
    return file_name