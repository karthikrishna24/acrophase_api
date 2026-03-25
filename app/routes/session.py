from app.crud import create_session, get_sessions_by_user
from app.database import get_db
from app.schemas import WorkoutSession, WorkoutSessionResponse
from fastapi import APIRouter, Depends, Query, Response, status
import logging
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/webhook/session", status_code=status.HTTP_201_CREATED)
def create_workout_session(session: WorkoutSession, response: Response, db: Session = Depends(get_db)):
    logger.info(f"Received webhook for session {session.session_id}")
    result = create_session(db, session)

    if result["created"]:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_201_CREATED

    return result


@router.get("/sessions", response_model=list[WorkoutSessionResponse])
def get_sessions(
    user_id: int, limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)
):
    sessions = get_sessions_by_user(db, user_id, limit, offset)
    return sessions
