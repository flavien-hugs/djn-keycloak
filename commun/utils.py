from typing import Optional, List, Any

from ninja import Schema
from ninja.pagination import PaginationBase


class CustomPagination(PaginationBase):
    class Input(Schema):
        page: Optional[int] = 1
        per_page: Optional[int] = 10

    class Output(Schema):
        results: List[Any]
        count: int
        page: int
        per_page: int

    items_attribute: str = "results"

    def paginate_queryset(self, queryset, pagination: Input, **params):
        per_page = pagination.per_page
        page = abs(per_page * (pagination.page - 1))

        return {
            "results": queryset[page : page + 10],
            "count": len(queryset),
            "page": pagination.page,
            "per_page": per_page,
        }
