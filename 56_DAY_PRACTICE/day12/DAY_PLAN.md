# DAY12 - FastAPI Basics

## Goal
Complete this day manually with verified outputs only.

## Working Files
- Manual build artifact: `main.py`
- Local verification file: `test_main.py`
- Reference only: `practice_session/02_main.py`

## Syllabus
- Core concept understanding
- Small build artifact
- One debug artifact
- Interview conversion (30s, 90s STAR, 3-min)

## Step-by-Step Plan
1. Create `/health` endpoint
2. Create `/echo` endpoint
3. Add request body model using Pydantic
4. Run one valid + one invalid request
5. Write 30s/90s/3-min interview answers

## Status Log (Update in this file)

| Block | Status | Start | End | Evidence |
|---|---|---|---|---|
| Step 1 | completed |  |  | `GET /health` returned `200` in `api_evidence.txt` |
| Step 2 | completed |  |  | valid `POST /echo` returned `200` in `api_evidence.txt` |
| Step 3 | completed |  |  | `EchoRequest` body model is implemented in `main.py` |
| Step 4 | completed |  |  | invalid `POST /echo` returned `422` in `api_evidence.txt` |
| Step 5 | completed | 2026-03-23 | 2026-03-23 | interview_pack_day12.md + practice_session/05_interview_answers.md |
| Day Closeout | completed | 2026-03-23 | 2026-03-23 | All artifacts complete |

## Completion Criteria
- [x] Code/query artifact done
- [x] Debug artifact done
- [x] Interview artifact done
- [x] Progress files updated (DAILY_PROGRESS_LOG.md updated today)


## Topic Completion Checkboxes

- [x] Step 1: Create `/health` endpoint
- [x] Step 2: Create `/echo` endpoint
- [x] Step 3: Add request body model using Pydantic
- [x] Step 4: Run one valid + one invalid request
- [x] Step 5: Write 30s/90s/3-min interview answers
- [x] Day Closeout
