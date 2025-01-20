from .base_repository import BaseRepository
from app.db.models import User
from sqlalchemy.orm import Session

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
