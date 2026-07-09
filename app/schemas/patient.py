from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PatientRead(BaseModel):
    id: UUID
    external_patient_id: str
    year_of_birth: int | None
    sex: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

