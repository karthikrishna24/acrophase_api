from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class WorkoutSession(BaseModel):
    session_id: str
    user_id: int
    workout_name: str
    workout_type: str
    calories_burned: int
    start_time: datetime
    end_time: datetime

    @field_validator("end_time")
    def validate_time(cls, end_time, info):
        start_time = info.data.get("start_time")
        if start_time and end_time < start_time:
            raise ValueError("end_time must be greater than start_time")
        return end_time


class WorkoutSessionResponse(BaseModel):
    session_id: str
    user_id: int
    workout_name: str
    workout_type: str
    calories_burned: int
    duration_seconds: int
    start_time: datetime
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)
