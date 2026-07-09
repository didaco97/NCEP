from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Patient
from app.schemas.patient import PatientRead

router = APIRouter()


@router.get("", response_model=list[PatientRead])
def list_patients(db: Session = Depends(get_db), limit: int = 50, offset: int = 0) -> list[Patient]:
    statement = select(Patient).order_by(Patient.created_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement))

