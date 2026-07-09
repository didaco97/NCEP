from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def read_health(db: Session = Depends(get_db)) -> dict[str, str | int]:
    db_check = db.execute(text("SELECT 1")).scalar_one()
    return {"status": "ok", "database": "ok", "db_check": db_check}

