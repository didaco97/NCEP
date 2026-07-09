# NCEP Backend Local Setup

Follow these steps from a fresh clone to run the NCEP backend on your machine.

## What You Need First

Install these before starting:

- Python 3.12
- Docker Desktop
- Git

On Windows, use PowerShell for the commands below.

## Step 1: Clone The Repo

```powershell
git clone <repo-url>
cd <repo-folder>
```

If you already have the repo, just open a terminal in the repo root.

## Step 2: Start Docker Desktop

Open Docker Desktop and wait until it says Docker is running.

Check it from the terminal:

```powershell
docker --version
docker compose version
```

## Step 3: Create The Python Environment

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should now see `(.venv)` at the start of your terminal prompt.

## Step 4: Install Python Packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This may take a few minutes because the project includes scientific and ECG libraries.

## Step 5: Create Your Local .env File

```powershell
Copy-Item .env.example .env
```

Replace the placeholder password with a local-only password:

```powershell
(Get-Content .env) -replace '<local-dev-password>', 'ncep_dev_password' | Set-Content .env
```

This value is only for your local Docker database.

Do not put real secrets or real patient data in `.env`.

## Step 6: Start PostgreSQL

```powershell
docker compose up -d postgres
```

Check that it is healthy:

```powershell
docker compose ps
```

You should see `ncep-postgres` with a healthy/running status.

## Step 7: Run Database Migrations

```powershell
alembic upgrade head
```

This creates the first database tables:

- `users`
- `patients`
- `ecg_records`
- `reports`

## Step 8: Add Synthetic Test Data

```powershell
python -m scripts.seed_dev_data
```

This adds fake development data only. It does not use real patient data.

## Step 9: Run The Backend

```powershell
uvicorn app.main:app --reload
```

Keep this terminal open.

## Step 10: Check That It Works

Open a second terminal in the same repo folder.

Activate the virtual environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run these checks:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/api/v1/db-summary
Invoke-RestMethod http://127.0.0.1:8000/api/v1/patients
```

Expected result:

- `/health` shows `status: ok`
- `/api/v1/db-summary` shows at least 1 user, 1 patient, 1 ECG record, and 1 report
- `/api/v1/patients` returns the synthetic patient `SYNTH-NCEP-0001`

You can also open the API docs in your browser:

```text
http://127.0.0.1:8000/docs
```

## Daily Use After Setup

After the first setup, you usually only need these commands:

```powershell
.\.venv\Scripts\Activate.ps1
docker compose up -d postgres
alembic upgrade head
uvicorn app.main:app --reload
```

## Stop The Backend

In the terminal running Uvicorn, press:

```text
Ctrl + C
```

To stop PostgreSQL:

```powershell
docker compose down
```

## If Something Fails

Check Docker is running:

```powershell
docker compose ps
```

Check the Python environment:

```powershell
python --version
pip check
```

Check the database migration state:

```powershell
alembic current
```

Run lint checks:

```powershell
ruff check app alembic scripts
```

## Notes

- Use Python 3.12.
- Keep `.env` local only.
- Commit `.env.example`, not `.env`.
- Use only synthetic data for development.
- The pinned dependency list is in `requirements.txt`.
