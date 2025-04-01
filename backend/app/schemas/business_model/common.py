"""
Common Business Models

This file defines common business model types and utilities used across the application.

Dependencies:
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from typing import List, TypeVar, Generic

from pydantic import BaseModel, Field, ConfigDict

T = TypeVar('T')


class PaginationParameterModel(BaseModel):
    """
    Business model for pagination parameters

    Attributes:
        page_index (int): Current page number
        page_size (int): Items per page
    """
    page_index: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, default=10)


class PaginatedResultModel(BaseModel, Generic[T]):
    """
    Business model for paginated results

    Attributes:
        items (List[T]): Items in current page
        total_count (int): Total number of items
        page_index (int): Current page number
        page_size (int): Items per page
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    items: List[T]
    total_count: int
    page_index: int
    page_size: int

    @property
    def total_pages(self) -> int:
        """Calculate total number of pages"""
        return (self.total_count + self.page_size - 1) // self.page_size

    @property
    def has_previous(self) -> bool:
        """Check if previous page exists"""
        return self.page_index > 1

    @property
    def has_next(self) -> bool:
        """Check if next page exists"""
        return self.page_index < self.total_pages
