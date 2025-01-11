from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, obj_in):
        obj_db = self.model(**obj_in.dict())
        self.db.add(obj_db)
        self.db.commit()
        self.db.refresh(obj_db)
        return obj_db
