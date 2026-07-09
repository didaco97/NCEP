from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import ECGRecord, Patient, Report, User


def main() -> None:
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == "dev.clinician@example.test"))
        if user is None:
            user = User(
                email="dev.clinician@example.test",
                hashed_password="local-dev-placeholder-not-for-login",
                role="clinician",
            )
            db.add(user)
            db.flush()

        patient = db.scalar(select(Patient).where(Patient.external_patient_id == "SYNTH-NCEP-0001"))
        if patient is None:
            patient = Patient(external_patient_id="SYNTH-NCEP-0001", year_of_birth=1984, sex="not_specified")
            db.add(patient)
            db.flush()

        ecg_record = db.scalar(
            select(ECGRecord).where(ECGRecord.signal_file_reference == "synthetic/synth-ncep-0001-ecg.csv")
        )
        if ecg_record is None:
            ecg_record = ECGRecord(
                patient_id=patient.id,
                recorded_at=datetime(2026, 7, 9, 9, 0, tzinfo=UTC),
                source_device="synthetic-dev-generator",
                signal_file_reference="synthetic/synth-ncep-0001-ecg.csv",
                sample_rate=500.0,
                lead_config="12-lead",
                uploaded_by=user.id,
            )
            db.add(ecg_record)
            db.flush()

        report = db.scalar(select(Report).where(Report.ecg_record_id == ecg_record.id))
        if report is None:
            db.add(
                Report(
                    ecg_record_id=ecg_record.id,
                    created_by=user.id,
                    findings="Synthetic development report. No real patient data.",
                    status="draft",
                )
            )

        db.commit()


if __name__ == "__main__":
    main()

