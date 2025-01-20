from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import ConfigDict

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)

    def dict(self):
        """Convert model instance to dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
