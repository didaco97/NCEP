from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ECGRecord
from app.schemas.ecg_record import ECGRecordRead

router = APIRouter()


@router.get("", response_model=list[ECGRecordRead])
def list_ecg_records(db: Session = Depends(get_db), limit: int = 50, offset: int = 0) -> list[ECGRecord]:
    statement = select(ECGRecord).order_by(ECGRecord.recorded_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement))

