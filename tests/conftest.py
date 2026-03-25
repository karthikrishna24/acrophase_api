from app.database import Base, engine
import os
import pytest

# Hardcode test database environment variables
os.environ["DB_HOST"] = "test_db" if os.getenv("DB_HOST") == "test_db" else "localhost"
os.environ["DB_PORT"] = "5432" if os.getenv("DB_HOST") == "test_db" else "5434"
os.environ["DB_NAME"] = "acrophase_test"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "admin"  # noqa S105 - This is only for testing purposes and not used in production


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)
