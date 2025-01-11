from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type
from contextlib import contextmanager

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def begin_transaction(self):
        return self.db.begin()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    @contextmanager
    def transaction(self):
        try:
            yield
            self.commit()
        except Exception:
            self.rollback()
            raise

    def get(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, obj_in):
        with self.transaction():
            obj_db = self.model(**obj_in.dict())
            self.db.add(obj_db)
            self.db.flush()
            self.db.refresh(obj_db)
            return obj_db

    def update(self, id: int, obj_in: dict):
        with self.transaction():
            self.db.query(self.model).filter(self.model.id == id).update(obj_in)
            return self.get(id)

    def delete(self, id: int):
        with self.transaction():
            obj_db = self.get(id)
            if obj_db:
                self.db.delete(obj_db)
            return obj_db
