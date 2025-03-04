from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
