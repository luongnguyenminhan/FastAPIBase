"""
Base Model Definition

This file defines the base model class for all database models.
It includes common fields and methods for all models.

Dependencies:
- SQLAlchemy for database operations
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import ConfigDict

Base = declarative_base()


class BaseModel(Base):
    """
    Base model class for all database models

    Attributes:
        id (int): The primary key of the model
        create_date (DateTime): The creation date of the model
        update_date (DateTime): The last update date of the model
        is_deleted (bool): The deletion status of the model
    """
    __abstract__ = True

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.now(timezone("Asia/Ho_Chi_Minh")))
    update_date = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)

    def dict(self):
        """
        Convert model instance to dictionary

        Returns:
            dict: A dictionary representation of the model instance
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
