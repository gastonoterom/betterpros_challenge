from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import create_tables


def get_mock_session():
    test_engine = create_engine("sqlite+pysqlite:///:memory:",
                                connect_args={"check_same_thread": False}, echo=False, future=True)

    TestSessions = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine)

    create_tables(test_engine)

    return TestSessions()
