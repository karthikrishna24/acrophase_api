# Acrophase Workout Session API

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Makefile
- PostgreSQL (or update `.env` with your database host)

### Setup
```bash
cp .sample.env .env  # Edit .env with your database config
```

## Running

- Make sure build is done

**Start the service:**
```bash
make start
```

**Stop the service:**
```bash
make stop
```

**Run tests:**
```bash
make test
```

## API Endpoints

### POST /webhook/session
Store a workout session (idempotent).

**Request:**
```json
{
  "session_id": "177442450245",
  "user_id": 1,
  "workout_name": "run",
  "workout_type": "cardio",
  "calories_burned": 250,
  "start_time": "2026-03-25T06:00:00Z",
  "end_time": "2026-03-25T06:30:00Z"
}
```

**Response (201/200):**
```json
{
  "message": "177442450245 Session stored successfully",
  "created": true
}
```

### GET /sessions
Retrieve sessions for a user with pagination.

**Query Params:**
- `user_id` (required)
- `limit` (optional, default: 10, max: 100)
- `offset` (optional, default: 0)

**Request:**
```
GET /sessions?user_id=1&limit=10&offset=0
```

**Response:**
```json
{
  "items": [
    {
      "session_id": "177442456243",
      "user_id": 1,
      "workout_name": "Morning Run",
      "workout_type": "cardio",
      "calories_burned": 250,
      "duration_seconds": 1800,
      "start_time": "2026-03-25T06:00:00Z",
      "end_time": "2026-03-25T06:30:00Z"
    },
    {
        "session_id": "177442456245",
        "user_id": 1,
        "workout_name": "run",
        "workout_type": "cardio",
        "calories_burned": 260,
        "duration_seconds": 1920,
        "start_time": "2026-03-26T11:30:00",
        "end_time": "2026-03-26T12:02:00"
    }
    .
    .
    .
    .
  ]
}
```

## Logs

Logs are printed to console. Control verbosity via `LOG_LEVEL` in `.env`:
- `DEBUG`: Detailed info
- `INFO`: General info (default)
- `WARNING`: Warnings only
- `ERROR`: Errors only
