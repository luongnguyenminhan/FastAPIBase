from app.db.models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    items_count = Column(Integer, default=0)

    items = relationship("Item", back_populates="owner")
