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
Last Modified: Current Date
Version: 1.0.2
"""

from contextlib import contextmanager

# Removed import for ItemRepository
from app.repositories.google_auth_repository import GoogleAuthRepository
from sqlalchemy.orm import Session


class UnitOfWork:
    """
    Unit of Work implementation for managing database transactions and repositories.

    Attributes:
        _session (Session): SQLAlchemy database session
        _transaction: Active database transaction
        _google_auth_repository (GoogleAuthRepository): Lazy-loaded Google authentication repository
        # Removed _item_repository attribute
    """

    def __init__(self, session: Session):
        """
        Initialize the Unit of Work

        Args:
            session (Session): SQLAlchemy session
        """
        self._session = session
        self._transaction = None

        # Repository instances
        self._google_auth_repository = None
        # Removed _item_repository initialization

    @property
    def google_auth_repository(self) -> GoogleAuthRepository:
        """
        Access the lazy-loaded Google authentication repository

        Returns:
            GoogleAuthRepository: Instance of the Google authentication repository
        """
        if not self._google_auth_repository:
            self._google_auth_repository = GoogleAuthRepository(self._session)
        return self._google_auth_repository

    # Removed item_repository property

    def begin(self):
        """
        Begin a new transaction

        Creates a new database transaction if one is not already active
        """
        self._transaction = self._session.begin()

    def commit(self):
        """
        Commit the changes in the current transaction

        Raises:
            Exception: When an error occurs during commit,
                      automatically rolls back and raises the exception
        """
        try:
            self._session.flush()
            if self._transaction:
                self._transaction.commit()
        except Exception:
            self.rollback()
            raise

    def rollback(self):
        """
        Rollback the changes in the current transaction

        Ensures that all changes are rolled back when an error occurs
        """
        if self._transaction:
            self._transaction.rollback()

    def save(self):
        """
        Save changes to the database

        Flushes pending changes to the database without committing the transaction
        """
        self._session.flush()

    @contextmanager
    def transaction(self):
        """
        Context manager for managing transaction scope

        Provides:
            - Automatic transaction start
            - Automatic commit on success
            - Automatic rollback on error
            - Automatic session closing

        Raises:
            Exception: Any exception occurring within the transaction block
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
