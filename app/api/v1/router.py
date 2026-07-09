from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.v1.routes import ecg_records, patients, reports, users
from app.db.session import get_db
from app.models import ECGRecord, Patient, Report, User

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(ecg_records.router, prefix="/ecg-records", tags=["ecg-records"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])


@api_router.get("/db-summary", tags=["health"])
def read_db_summary(db: Session = Depends(get_db)) -> dict[str, int]:
    return {
        "users": db.scalar(select(func.count()).select_from(User)) or 0,
        "patients": db.scalar(select(func.count()).select_from(Patient)) or 0,
        "ecg_records": db.scalar(select(func.count()).select_from(ECGRecord)) or 0,
        "reports": db.scalar(select(func.count()).select_from(Report)) or 0,
    }

