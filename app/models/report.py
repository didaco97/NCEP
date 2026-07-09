from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.ecg_record import ECGRecord
    from app.models.user import User


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (CheckConstraint("status IN ('draft', 'final', 'amended')", name="ck_reports_status"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ecg_record_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ecg_records.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    findings: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    signed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    ecg_record: Mapped["ECGRecord"] = relationship(back_populates="reports")
    author: Mapped["User | None"] = relationship(back_populates="reports")
