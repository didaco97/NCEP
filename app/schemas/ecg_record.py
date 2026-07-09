from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ECGRecordRead(BaseModel):
    id: UUID
    patient_id: UUID
    recorded_at: datetime
    source_device: str | None
    signal_file_reference: str
    sample_rate: float
    lead_config: str
    uploaded_by: UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}

