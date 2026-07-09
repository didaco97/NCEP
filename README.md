# NCEP Backend

FastAPI backend for the NCEP development environment, with PostgreSQL, SQLAlchemy, Alembic migrations, and a starter schema for users, patient metadata, ECG records, and reports.

## Quick Start

Use Python 3.12 and Docker Desktop.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
(Get-Content .env) -replace '<local-dev-password>', 'ncep_dev_password' | Set-Content .env
docker compose up -d postgres
alembic upgrade head
python -m scripts.seed_dev_data
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Or verify from a second terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/api/v1/db-summary
Invoke-RestMethod http://127.0.0.1:8000/api/v1/patients
```

## Full Setup Guide

For step-by-step instructions, see:

[docs/setup/README.md](docs/setup/README.md)

The setup state ledger is here:

[docs/setup/NCEP_BACKEND_ENV_STATE.md](docs/setup/NCEP_BACKEND_ENV_STATE.md)


## Development Notes

- Keep `.env` local only.
- Commit `.env.example`, not `.env`.
- Use synthetic development data only.
- The pinned Python dependencies are in `requirements.txt`.
