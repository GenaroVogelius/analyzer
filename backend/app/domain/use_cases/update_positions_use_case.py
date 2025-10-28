from app.domain.interfaces.repositories.operations_repository_interface import (
    OperationProperties,
    OperationsRepositoryInterface,
)


class UpdatePositionsUseCase:
    """
    This use case is responsible of updating operations from the database.
    """

    def __init__(
        self,
        repository: OperationsRepositoryInterface,
    ):
        self.repository = repository

    async def execute(
        self,
        properties_to_filter: OperationProperties,
        properties_to_update: OperationProperties,
    ) -> int:
        updated_count = await self.repository.update_operations(
            properties_to_filter=properties_to_filter,
            properties_to_update=properties_to_update,
        )

        return updated_count
