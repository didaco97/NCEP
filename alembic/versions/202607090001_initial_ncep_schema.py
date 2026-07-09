"""Initial NCEP backend schema.

Revision ID: 202607090001
Revises:
Create Date: 2026-07-09 00:01:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "202607090001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="clinician"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "patients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("external_patient_id", sa.String(length=100), nullable=False),
        sa.Column("year_of_birth", sa.Integer(), nullable=True),
        sa.Column("sex", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("external_patient_id", name="uq_patients_external_patient_id"),
    )

    op.create_table(
        "ecg_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_device", sa.String(length=100), nullable=True),
        sa.Column("signal_file_reference", sa.String(length=500), nullable=False),
        sa.Column("sample_rate", sa.Float(), nullable=False),
        sa.Column("lead_config", sa.String(length=50), nullable=False),
        sa.Column("uploaded_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], name="fk_ecg_records_patient_id", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["uploaded_by"], ["users.id"], name="fk_ecg_records_uploaded_by", ondelete="SET NULL"),
    )
    op.create_index("ix_ecg_records_patient_id", "ecg_records", ["patient_id"])

    op.create_table(
        "reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("ecg_record_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("findings", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("status IN ('draft', 'final', 'amended')", name="ck_reports_status"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], name="fk_reports_created_by", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["ecg_record_id"], ["ecg_records.id"], name="fk_reports_ecg_record_id", ondelete="CASCADE"),
    )
    op.create_index("ix_reports_ecg_record_id", "reports", ["ecg_record_id"])


def downgrade() -> None:
    op.drop_index("ix_reports_ecg_record_id", table_name="reports")
    op.drop_table("reports")
    op.drop_index("ix_ecg_records_patient_id", table_name="ecg_records")
    op.drop_table("ecg_records")
    op.drop_table("patients")
    op.drop_table("users")

