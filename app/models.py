from app.database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String


class WorkoutSessionDB(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    workout_name = Column(String, nullable=False)
    workout_type = Column(String, nullable=False)
    calories_burned = Column(Integer, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
