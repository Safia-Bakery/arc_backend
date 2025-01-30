from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.kru_reports import get_kru_report, top50_excell_generator
from app.routes.depth import get_db, get_current_user
from app.schemas.kru_reports import KruReport
from app.schemas.users import GetUserFullData


kru_reports_router = APIRouter()




@kru_reports_router.post("/kru/reports/")
def get_reports(
        data: KruReport,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    query = get_kru_report(db=db, data=data)
    file_name = top50_excell_generator(
        data=query,
        report_type=data.report_type,
        start_date=data.start_date,
        finish_date=data.finish_date
    )
    return {'file_name': file_name}