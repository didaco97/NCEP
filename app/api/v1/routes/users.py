from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.schemas.user import UserRead

router = APIRouter()


@router.get("", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), limit: int = 50, offset: int = 0) -> list[User]:
    statement = select(User).order_by(User.created_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement))

