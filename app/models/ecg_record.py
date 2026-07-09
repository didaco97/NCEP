from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.patient import Patient
    from app.models.report import Report
    from app.models.user import User


class ECGRecord(Base):
    __tablename__ = "ecg_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_device: Mapped[str | None] = mapped_column(String(100), nullable=True)
    signal_file_reference: Mapped[str] = mapped_column(String(500), nullable=False)
    sample_rate: Mapped[float] = mapped_column(Float, nullable=False)
    lead_config: Mapped[str] = mapped_column(String(50), nullable=False)
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    patient: Mapped["Patient"] = relationship(back_populates="ecg_records")
    uploader: Mapped["User | None"] = relationship(back_populates="ecg_uploads")
    reports: Mapped[list["Report"]] = relationship(back_populates="ecg_record", cascade="all, delete-orphan")
