from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}

