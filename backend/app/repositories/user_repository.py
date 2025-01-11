from .base_repository import BaseRepository
from app.db.models import User  # Updated import
from sqlalchemy.orm import Session
from typing import Optional, List

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(self.model).filter(self.model.email == email).first()
    
    def get_active_users(self) -> List[User]:
        return self.db.query(self.model).filter(self.model.is_active == True).all()
    
    def update(self, id: int, update_data: dict):
        self.db.query(self.model).filter(self.model.id == id).update(update_data)
        self.db.commit()
    
    def delete(self, id: int):
        user = self.get(id)
        if user:
            self.db.delete(user)
            self.db.commit()
        return user
