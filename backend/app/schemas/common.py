"""
Common Schemas

This file defines common schemas used across the application, such as pagination parameters and results.

Dependencies:
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, TypeVar, Generic

T = TypeVar('T')


class PaginationParameter(BaseModel):
    """
    Schema for pagination parameters

    Attributes:
        page_index (int): The index of the current page, default is 1
        page_size (int): The number of items per page, default is 10
    """
    page_index: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, default=10)


class Pagination(BaseModel, Generic[T]):
    """
    Schema for paginated results

    Attributes:
        items (List[T]): The list of items on the current page
        total_count (int): The total number of items
        page_index (int): The index of the current page
        page_size (int): The number of items per page
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    items: List[T]
    total_count: int
    page_index: int
    page_size: int

    @property
    def total_pages(self) -> int:
        """
        Calculate the total number of pages

        Returns:
            int: The total number of pages
        """
        return (self.total_count + self.page_size - 1) // self.page_size

    @property
    def has_previous(self) -> bool:
        """
        Check if there is a previous page

        Returns:
            bool: True if there is a previous page, False otherwise
        """
        return self.page_index > 1

    @property
    def has_next(self) -> bool:
        """
        Check if there is a next page

        Returns:
            bool: True if there is a next page, False otherwise
        """
        return self.page_index < self.total_pages
