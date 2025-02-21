from sqlalchemy.orm import sessionmaker, scoped_session
from src.db.db import connect_with_connector

# Create an engine instance
engine = connect_with_connector()

# Create a session factory for async sessions
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

SessionScoped = scoped_session(SessionLocal)

def get_db():
    db = SessionScoped()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
