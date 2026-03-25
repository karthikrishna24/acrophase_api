from app.models import WorkoutSessionDB
from app.schemas import WorkoutSession
import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def create_session(db: Session, session_data: WorkoutSession):
    """
    Create a workout session (idempotent)
    """

    duration_seconds = int((session_data.end_time - session_data.start_time).total_seconds())

    db_session = WorkoutSessionDB(
        session_id=session_data.session_id,
        user_id=session_data.user_id,
        workout_name=session_data.workout_name,
        workout_type=session_data.workout_type,
        calories_burned=session_data.calories_burned,
        start_time=session_data.start_time,
        end_time=session_data.end_time,
        duration_seconds=duration_seconds,
    )

    try:
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        logger.info(f"Session {session_data.session_id} created successfully")
        return {"message": f"{session_data.session_id} Session stored successfully", "created": True}

    except IntegrityError:
        db.rollback()
        logger.warning(f"Duplicate session {session_data.session_id} attempted")
        return {"message": f"{session_data.session_id} Session already exists", "created": False}

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error for session {session_data.session_id}: {str(e)}")
        return {"message": "Database error occurred", "created": False}


def get_sessions_by_user(db: Session, user_id: int, limit: int, offset: int):
    """
    Fetch sessions for a user with pagination
    """

    sessions = (
        db.query(WorkoutSessionDB)
        .filter(WorkoutSessionDB.user_id == user_id)
        .order_by(WorkoutSessionDB.start_time.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return sessions
