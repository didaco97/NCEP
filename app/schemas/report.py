from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReportRead(BaseModel):
    id: UUID
    ecg_record_id: UUID
    created_by: UUID | None
    findings: str
    status: str
    created_at: datetime
    signed_at: datetime | None

    model_config = {"from_attributes": True}

