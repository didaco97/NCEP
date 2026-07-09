from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Report
from app.schemas.report import ReportRead

router = APIRouter()


@router.get("", response_model=list[ReportRead])
def list_reports(db: Session = Depends(get_db), limit: int = 50, offset: int = 0) -> list[Report]:
    statement = select(Report).order_by(Report.created_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement))

