from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# In memory sql database for challenge purposes
engine = create_engine("sqlite+pysqlite:///:memory:",
                       connect_args={"check_same_thread": False}, echo=True, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
