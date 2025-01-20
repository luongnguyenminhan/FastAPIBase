from .base_repository import BaseRepository
from app.db.models import User
from sqlalchemy.orm import Session

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
        
    def get_by_email(self, email: str) -> User:
        return self._dbSet.filter_by(email=email, is_deleted=False).first()
    
    def get_active_users(self):
        return self._dbSet.filter_by(is_active=True, is_deleted=False).all()
