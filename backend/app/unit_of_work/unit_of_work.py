from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.repositories.item_repository import ItemRepository
from contextlib import contextmanager

class UnitOfWork:
    def __init__(self, session: Session):
        self._session = session
        self._transaction = None
        
        # Repository instances
        self._user_repository = None
        self._item_repository = None

    @property
    def user_repository(self) -> UserRepository:
        if not self._user_repository:
            self._user_repository = UserRepository(self._session)
        return self._user_repository

    @property
    def item_repository(self) -> ItemRepository:
        if not self._item_repository:
            self._item_repository = ItemRepository(self._session)
        return self._item_repository

    def begin(self):
        self._transaction = self._session.begin()

    def commit(self):
        try:
            self._session.commit()
            if self._transaction:
                self._transaction.commit()
        except Exception:
            self.rollback()
            raise

    def rollback(self):
        if self._transaction:
            self._transaction.rollback()
            
    def save(self):
        self._session.save()

    @contextmanager
    def transaction(self):
        """Provide a transactional scope around a series of operations."""
        try:
            self.begin()
            yield
            self.commit()
        except Exception:
            self.rollback()
            raise
        finally:
            self._session.close()
