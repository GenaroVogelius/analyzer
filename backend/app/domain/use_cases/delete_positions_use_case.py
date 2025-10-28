from app.domain.entities.enums import HBTypeOperations
from app.domain.interfaces.repositories.operations_repository_interface import (
    OperationsRepositoryInterface,
)


class DeletePositionsUseCase:
    """
    This use case is responsible of deleting operations from the database.
    """

    def __init__(
        self,
        repository: OperationsRepositoryInterface,
    ):
        self.repository = repository

    async def execute(
        self,
        id: list[int] | None = None,
        ticker: list[str] | None = None,
        type_operation: tuple[HBTypeOperations, ...] | None = None,
    ) -> int:
        deleted_count = await self.repository.delete_operations(
            id=id,
            ticker=ticker,
            type_operation=type_operation,
        )

        return deleted_count
