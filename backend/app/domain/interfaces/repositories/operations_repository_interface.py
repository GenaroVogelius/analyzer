import datetime
from abc import abstractmethod
from typing import NotRequired, Protocol, TypedDict

from app.domain.entities.entities import Operation
from app.domain.entities.enums import HBTypeOperations


class OperationProperties(TypedDict, total=False):
    """TypedDict for Operation entity properties that can be used for filtering and updating."""

    id: NotRequired[int]
    code: NotRequired[str]
    accumulated: NotRequired[float]
    number_receipt: NotRequired[int]
    date_liquidation: NotRequired[datetime.date]
    date_operation: NotRequired[datetime.date]
    import_of_operation: NotRequired[float]
    comprobant_of_operation: NotRequired[int]
    amount: NotRequired[float]
    price_of_operation: NotRequired[float]


class OperationsRepositoryInterface(Protocol):
    """
    Interface for operations repository, it has methods for CRUD operations.
    """

    @abstractmethod
    async def create_operations(self, operations: list[Operation]):
        """
        Create operations.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_operations(
        self,
        from_date: datetime.date,
        to_date: datetime.date,
        type_operation: tuple[HBTypeOperations, ...] | None = None,
        ticker: str | None = None,
    ) -> list[Operation]:
        """
        Get operations.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_operations(
        self,
        properties_to_filter: OperationProperties,
        properties_to_update: OperationProperties,
    ) -> int:
        """
        Update operations.

        Args:
            properties_to_filter: OperationProperties dictionary used as filters
            properties_to_update: OperationProperties dictionary with values to update
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_operations(
        self,
        id: list[int] | None = None,
        ticker: list[str] | None = None,
        type_operation: tuple[HBTypeOperations, ...] | None = None,
    ):
        """
        Delete operations.
        At least one parameter is required. If multiple parameters are provided,
        they will be used as filters to delete operations that match all criteria.
        """
        raise NotImplementedError
