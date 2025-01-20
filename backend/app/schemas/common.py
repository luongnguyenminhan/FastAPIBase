from pydantic import BaseModel, Field, ConfigDict
from typing import List, TypeVar, Generic

T = TypeVar('T')

class PaginationParameter(BaseModel):
    page_index: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, default=10)

class Pagination(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    items: List[T]
    total_count: int
    page_index: int
    page_size: int
    
    @property
    def total_pages(self) -> int:
        return (self.total_count + self.page_size - 1) // self.page_size

    @property
    def has_previous(self) -> bool:
        return self.page_index > 1

    @property
    def has_next(self) -> bool:
        return self.page_index < self.total_pages
