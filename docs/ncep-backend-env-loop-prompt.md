# NCEP Backend Dev Environment -- Codex Loop Engineering Prompt Pack

**What this is:** a complete loop -- goal, state, skill, sub-agents, worktree, connectors -- for driving Codex to set up, verify, and document the NCEP backend's local dev environment, structured per [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) (Addy Osmani, Jun 2026). Drop the files below into the repo at the paths shown, then follow Section 7 to run it.

**Quick start:** paste Section 1 with `/goal`, then paste Section 6 as your next message in Codex. Everything else here is the supporting config those two prompts lean on.

## How this maps to a loop

| Building block | This loop |
|---|---|
| **Automation** (heartbeat) | A one-shot `/goal` run (or a single Automation run) drives setup to completion -- this is "run until done," not a recurring cron. Section 8 adds an optional recurring piece. |
| **Worktree** | Isolated branch, e.g. `feature/ncep-backend-env-setup` |
| **Skill** | `.agents/skills/ncep-backend-env/SKILL.md` -- NCEP's conventions written down once instead of re-derived every run |
| **Sub-agents** | `ncep_explorer` -> `ncep_builder` -> `ncep_verifier` -- maker and checker are different agents |
| **Connectors** | Postgres (MCP if you have it, else plain `psql`/Alembic) + GitHub (open the PR) |
| **State** | `docs/setup/NCEP_BACKEND_ENV_STATE.md` -- the ledger the loop reads and writes every turn |

---

## 1. The Goal contract

Paste this with `/goal` to start (see Section 7 if `/goal` isn't available in your build yet):

```text
/goal Stand up a working NCEP backend development environment on this repo and produce team-facing setup docs. Don't stop until every row in docs/setup/NCEP_BACKEND_ENV_STATE.md is checked off with real evidence.

Outcome: A developer can clone this repo, follow docs/setup/README.md, and within ~15 minutes have a FastAPI backend running locally against a real PostgreSQL database, with the initial schema (users, patient metadata, ECG records, reports) migrated in.

Verification surface:
- Fresh install (venv + requirements.txt, or the repo's existing pyproject.toml tool) completes with no errors.
- `alembic upgrade head` runs clean against a local/dockerized Postgres defined by .env.
- `uvicorn app.main:app --reload` boots; GET /health (or /docs) returns 200.
- A DB-backed endpoint returns real rows from Postgres -- proof the app-to-DB path works end to end, not just that each piece boots alone.
- docs/setup/NCEP_BACKEND_ENV_STATE.md shows every row checked off with a one-line evidence note (command run + result).

Constraints:
- No real patient data, secrets, or a populated .env committed -- .env.example with placeholders only.
- Match whatever NCEP conventions already exist in this repo instead of inventing a parallel one -- read before you write.
- Keep dependencies boring and version-pinned; verify current stable versions rather than assuming.

Boundaries:
- Work on a dedicated branch/worktree, not main.
- You may install packages, run local Postgres (e.g. via Docker), run migrations, run the app locally.
- No deploys, no CI/CD changes, no edits to unrelated services beyond reading their conventions.
```

## 2. State ledger

`docs/setup/NCEP_BACKEND_ENV_STATE.md` -- create this first; every sub-agent reads and updates it.

```markdown
# NCEP Backend Dev Environment -- Setup State

Legend: not started / in progress / done / blocked

| # | Deliverable | Status | Evidence | Notes |
|---|---|---|---|---|
| 1 | Python 3.12 installed & configured | not started | | |
| 2 | Required libraries identified & documented | not started | | |
| 3 | FastAPI project structure scaffolded | not started | | |
| 4 | PostgreSQL configured & connected | not started | | |
| 5 | Initial schema: users, patient metadata, ECG records, reports | not started | | |
| 6 | .env / .env.example created | not started | | |
| 7 | requirements.txt or pyproject.toml finalized | not started | | |
| 8 | Local run verified against real Postgres | not started | | |
| 9 | Setup fully documented for the team | not started | | |
| 10 | Confirmed aligned with existing NCEP architecture | not started | | |
```

## 3. Skill: NCEP backend environment conventions

`.agents/skills/ncep-backend-env/SKILL.md` (repo-root skill; if NCEP is a monorepo, put it under the backend service's own `.agents/skills/` instead).

```markdown
---
name: ncep-backend-env
description: Use when installing, configuring, or documenting the NCEP backend's local dev environment - Python 3.12/FastAPI/PostgreSQL setup, dependency list, project layout, .env, or the users/patient-metadata/ECG-records/reports schema. Not for frontend, deploy, or CI/CD tasks.
---

# NCEP Backend Environment Conventions

## Runtime
Python 3.12, via pyenv or a system install plus `venv`. Don't use conda for this service.

## Package manager
Check the repo first - if it already has a pyproject.toml with poetry/uv, use that. Otherwise default to requirements.txt + pip. Don't introduce a second package manager alongside an existing one.

## Dependencies by category
(verify current stable versions before pinning - don't trust versions from memory, including a prior agent's)

- Web: fastapi, uvicorn[standard]
- Validation/settings: pydantic, pydantic-settings
- Database: sqlalchemy>=2.0, alembic, psycopg[binary] (or psycopg2-binary if the repo already uses psycopg2)
- Scientific: numpy, pandas, scipy
- Biosignal/ECG: wfdb, neurokit2, biosppy
- Medical imaging: pydicom
- Auth: match whatever the repo already uses; if starting fresh, passlib[bcrypt] + python-jose[cryptography]
- Testing: pytest, pytest-asyncio, httpx
- Dev tooling: ruff

## Project structure (if none exists yet)
```
app/
  main.py
  core/             config.py (Settings via pydantic-settings), security.py
  api/v1/routes/    patients.py, ecg_records.py, reports.py, users.py
  models/           SQLAlchemy ORM models
  schemas/          Pydantic schemas
  services/         business logic
  db/               session.py, base.py
alembic/versions/
tests/
docs/setup/
```

## Schema starting point
Sketch only - finalize as real Alembic migrations against Postgres, and match any existing NCEP data model before adding a new one.

- users: id, email, hashed_password, role, created_at
- patients: id, external/MRN id, de-identified demographics, created_at
- ecg_records: id, patient_id -> patients.id, recorded_at, source_device, signal file reference, sample_rate, lead_config, uploaded_by -> users.id
- reports: id, ecg_record_id -> ecg_records.id, created_by -> users.id, findings, status (draft/final/amended), created_at, signed_at

Relationships: patient 1-N ecg_records; ecg_record 1-N reports; user 1-N reports (author).

## Data sensitivity
ECG + patient metadata is health data. Never put real PHI in .env, fixtures, or seed data - synthetic/faker-generated values only. .env stays gitignored; only .env.example is committed.

## Before building anything
Check for ARCHITECTURE.md, docs/architecture/, or an existing service in this repo/org, and match its conventions (naming, session handling, migration tooling, auth pattern) instead of introducing a second standard.

## Reference requirements.txt (starting point, not a lockfile)

fastapi
uvicorn[standard]
pydantic
pydantic-settings
sqlalchemy>=2.0
alembic
psycopg[binary]
numpy
pandas
scipy
wfdb
neurokit2
biosppy
pydicom
passlib[bcrypt]
python-jose[cryptography]
pytest
pytest-asyncio
httpx
ruff
```

## 4. Sub-agents: explorer -> builder -> verifier

`.codex/agents/ncep-explorer.toml`
```toml
name = "ncep_explorer"
description = "Read-only scout that maps existing NCEP architecture, conventions, and repo layout before any backend-env changes are made."
sandbox_mode = "read-only"
model_reasoning_effort = "medium"
developer_instructions = """
Before any setup work happens, map what already exists.
Look for ARCHITECTURE.md, docs/architecture/, existing services, an existing ORM/session pattern, an existing auth pattern, and any existing .env.example or CI config that hints at real conventions.
Report: conventions to reuse, gaps that block a clean setup, and conflicts the builder should flag rather than guess through.
Do not propose fixes yourself and do not edit files. Cite exact file paths.
"""
```

`.codex/agents/ncep-builder.toml`
```toml
name = "ncep_builder"
description = "Implementation agent for the NCEP backend dev environment: Python/FastAPI setup, PostgreSQL connection, schema, .env, dependency manifest."
sandbox_mode = "workspace-write"
model_reasoning_effort = "high"
developer_instructions = """
Work through docs/setup/NCEP_BACKEND_ENV_STATE.md top to bottom.
Follow the ncep-backend-env skill and whatever conventions ncep_explorer reported - don't introduce a second convention when one already exists.
After each deliverable, update its row in the state file with an evidence line (the exact command run and its result) before moving to the next.
Never commit secrets or real patient data - .env.example only, with placeholders.
If something needs a human call (package manager, auth pattern), log it as a Note and keep moving on unblocked items instead of stalling the whole loop.
"""
```

`.codex/agents/ncep-verifier.toml`
```toml
name = "ncep_verifier"
description = "Independent checker for the NCEP backend dev environment loop. Confirms each deliverable against its real verification command; doesn't trust the builder's self-report."
sandbox_mode = "workspace-write"
model_reasoning_effort = "high"
developer_instructions = """
For every row ncep_builder marks done, re-run the actual verification command yourself - don't accept a written claim as proof.
Send a row back to in-progress with a concrete reason if the command fails, if secrets/PHI show up anywhere they shouldn't, or if the change ignored a convention ncep_explorer reported.
Only mark the goal achieved when every row is genuinely done with real command output behind it.
"""
```

`.codex/config.toml` (add to whatever's already there)
```toml
[agents]
max_threads = 6
max_depth = 1

# Optional - only if you already have a Postgres MCP connector.
# Without this, ncep_builder/ncep_verifier just shell out to psql/alembic directly, which is fine.
# [mcp_servers.postgres]
# url = "http://localhost:PORT/mcp"
```

Leave `model` unset on all three agents so they inherit your session default -- set it explicitly per agent later if you want to trade cost against quality (e.g. a cheaper model for `ncep_explorer`, a stronger one for `ncep_verifier`).

## 5. Worktree & connectors

- **Worktree:** run this on its own branch/worktree (`feature/ncep-backend-env-setup`), not on `main` or on top of anyone's in-progress checkout. Running it as an Automation instead of interactively? Choose "background worktree," not "local checkout."
- **Postgres:** use an MCP connector if the team has one; otherwise the agents shell out to `psql`/`alembic` directly -- no connector required.
- **GitHub:** opens the PR once the goal is achieved (`gh pr create`, or Codex's GitHub integration).
- **Optional:** a Slack or Linear connector to post "NCEP backend dev env is ready -- see PR #___" once done, closing the loop on "share it with the team."
- If the repo already has an `AGENTS.md`, add a pointer to the skill and the state file there so future Codex sessions in this repo pick this context up automatically.

## 6. The orchestrator prompt

Paste this as your message right after setting the Goal in Section 1:

```text
$ncep-backend-env

Set up the NCEP backend local development environment in this repo end-to-end against a real PostgreSQL instance, then document it for the team.

1. Spawn ncep_explorer first. Wait for its report on existing NCEP conventions before touching anything.
2. Create docs/setup/NCEP_BACKEND_ENV_STATE.md from the template in the ncep-backend-env skill if it doesn't exist yet.
3. Spawn ncep_builder to work through the state file: Python 3.12 environment, the categorized dependency list (FastAPI, Uvicorn, SQLAlchemy, Pydantic, NumPy, Pandas, SciPy, WFDB, NeuroKit2, BioSPPy, PyDICOM, plus whatever auth/testing/lint tooling matches existing conventions), the FastAPI project structure, PostgreSQL connection + Alembic migrations, the initial schema for users/patient metadata/ECG records/reports, .env.example, and requirements.txt (or pyproject.toml).
4. After ncep_builder finishes each deliverable, spawn ncep_verifier to independently re-check it against real command output, not the builder's written claim.
5. Repeat steps 3-4 deliverable by deliverable until every row in the state file is checked off.
6. Once everything passes, write docs/setup/README.md: a complete, copy-pasteable setup guide (prereqs, install steps, .env instructions, running migrations, starting the server, verifying it works) so any teammate can follow it standalone.
7. Open a PR with all of this, summarizing what was set up and linking the state file and docs/setup/README.md.
8. Report back with the PR link and a summary of anything flagged as a judgment call for a human.

Work on a dedicated branch/worktree, not main. Never commit real secrets or patient data.
```

## 7. How to run it

1. Add the skill, the three agent files, and the `[agents]` block above to the repo at the paths shown (commit them, or keep local until reviewed).
2. `cd` into the repo and open Codex (CLI or app).
3. Using `/goal`: confirm `codex --version` is 0.128.0+ and `/goal` shows up in the slash menu. If not, run `codex features enable goals` (or add `features.goals = true` under `~/.codex/config.toml`) and restart.
4. Paste Section 1 with `/goal`, then paste Section 6 as your next message.
5. Prefer the Automations tab instead? Create a one-shot (non-recurring) Automation with Section 6 as the prompt, environment set to background worktree, and skip `/goal` entirely.
6. Review the resulting PR like any other PR -- a loop's checkmark is a claim backed by a command, not a merge approval.

## 8. Optional: keep it a real loop

Once the one-time setup lands, a recurring Automation (weekly, same repo, prompt: "re-run the verification surface in docs/setup/NCEP_BACKEND_ENV_STATE.md against a fresh checkout and Triage anything that no longer passes") catches environment drift -- a new required env var that didn't get documented, a migration that stops applying cleanly to a fresh DB -- before it costs someone a day. This part is genuinely optional; the core ask is a one-time setup, not a recurring job.

## 9. Caveats

- `/goal` is newer and sometimes feature-flagged depending on your Codex build -- Section 7 covers enabling it; the Automations path works either way.
- Sub-agents cost more tokens than one agent doing everything -- worth it here because `ncep_verifier` catching a bad migration before it reaches Postgres is cheap insurance, but don't reflexively add more agents than this.
- Nothing here assumes what NCEP's existing architecture looks like -- that's exactly why `ncep_explorer` runs first and reads your real docs instead of guessing.

---
Sources: [Loop Engineering -- Addy Osmani](https://addyosmani.com/blog/loop-engineering/) - [Codex: Subagents](https://developers.openai.com/codex/subagents) - [Codex: Automations](https://developers.openai.com/codex/app/automations) - [Codex: Skills](https://developers.openai.com/codex/skills) - [Codex Cookbook: Using Goals](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)

