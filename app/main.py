from app.database import Base, engine
from app.routes import session
from fastapi import FastAPI

app = FastAPI(title="acrophase workout session")

Base.metadata.create_all(bind=engine)

app.include_router(session.router)
