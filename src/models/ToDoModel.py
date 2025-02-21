from sqlalchemy import Column, Integer, String, Date
from src.db.base import Base

class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  
    title = Column(String, index=True)
    description = Column(String, index=True)
    due_date = Column(Date, index=True)  