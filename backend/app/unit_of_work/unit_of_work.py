"""
Unit of Work Pattern Implementation

This file implements the Unit of Work pattern for managing database transactions
and repository access. It provides a consistent interface for:
- Managing database transactions
- Accessing repositories
- Ensuring data consistency
- Handling rollbacks on failures

The Unit of Work pattern helps maintain data integrity by:
1. Coordinating multiple database operations in a single transaction
2. Providing atomic operations
3. Managing the lifecycle of database transactions
4. Centralizing transaction management logic

Dependencies:
- SQLAlchemy for database operations
- Repository implementations
- Contextlib for context manager support

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.repositories.item_repository import ItemRepository
from contextlib import contextmanager


class UnitOfWork:
    """
    Unit of Work implementation for managing database transactions and repositories.

    Attributes:
        _session (Session): SQLAlchemy database session
        _transaction: Active database transaction
        _user_repository (UserRepository): Lazy-loaded user repository
        _item_repository (ItemRepository): Lazy-loaded item repository
    """

    def __init__(self, session: Session):
        """
        Khởi tạo Unit of Work mới

        Args:
            session (Session): Phiên làm việc SQLAlchemy
        """
        self._session = session
        self._transaction = None

        # Repository instances
        self._user_repository = None
        self._item_repository = None

    @property
    def user_repository(self) -> UserRepository:
        """
        Truy cập lazy-loaded repository người dùng

        Returns:
            UserRepository: Instance của repository người dùng
        """
        if not self._user_repository:
            self._user_repository = UserRepository(self._session)
        return self._user_repository

    @property
    def item_repository(self) -> ItemRepository:
        """
        Truy cập lazy-loaded repository mục

        Returns:
            ItemRepository: Instance của repository mục
        """
        if not self._item_repository:
            self._item_repository = ItemRepository(self._session)
        return self._item_repository

    def begin(self):
        """
        Bắt đầu một giao dịch mới

        Tạo một giao dịch cơ sở dữ liệu mới nếu chưa có giao dịch nào đang hoạt động
        """
        self._transaction = self._session.begin()

    def commit(self):
        """
        Xác nhận các thay đổi trong giao dịch hiện tại

        Raises:
            Exception: Khi có lỗi xảy ra trong quá trình xác nhận,
                      tự động rollback và đẩy ngoại lệ lên
        """
        try:
            self._session.commit()
            if self._transaction:
                self._transaction.commit()
        except Exception:
            self.rollback()
            raise

    def rollback(self):
        """
        Hoàn tác các thay đổi trong giao dịch hiện tại

        Đảm bảo rằng tất cả các thay đổi được hoàn tác khi có lỗi xảy ra
        """
        if self._transaction:
            self._transaction.rollback()

    def save(self):
        """
        Lưu các thay đổi vào cơ sở dữ liệu

        Ghi các thay đổi đang chờ vào cơ sở dữ liệu mà không xác nhận giao dịch
        """
        self._session.save()

    @contextmanager
    def transaction(self):
        """
        Context manager để quản lý phạm vi giao dịch

        Provides:
            - Tự động bắt đầu giao dịch
            - Tự động xác nhận khi thành công
            - Tự động rollback khi có lỗi
            - Tự động đóng session

        Raises:
            Exception: Bất kỳ ngoại lệ nào xảy ra trong khối giao dịch
        """
        try:
            self.begin()
            yield
            self.commit()
        except Exception:
            self.rollback()
            raise
        finally:
            self._session.close()
