from src.database.db_engine import SessionLocal

def session_factory():
    return SessionLocal()
