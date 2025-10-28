import datetime
from typing import TYPE_CHECKING, Any

from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from app.domain.entities.entities import Operation
from app.domain.entities.enums import HBTypeOperations
from app.domain.interfaces.repositories.operations_repository_interface import (
    OperationsRepositoryInterface,
)

if TYPE_CHECKING:
    from app.domain.interfaces.repositories.operations_repository_interface import (
        OperationProperties,
    )

from app.infrastructure.db.postgresql.models import (
    OperationModel,
    OperationTypeModel,
    ReferenceModel,
    TicketModel,
)


class OperationsRepository(OperationsRepositoryInterface):
    async def create_operations(self, operations: list[Operation]) -> int:
        """
        Create operations.
        """
        async with in_transaction():
            operations_records = []
            for operation in operations:
                # Create and save related models first
                operation_type, _ = await OperationTypeModel.get_or_create(
                    type_operation=operation.type_operation.type_operation,
                    defaults={
                        "type_operation": operation.type_operation.type_operation
                    },
                )

                ticket, _ = await TicketModel.get_or_create(
                    ticker=operation.ticket.ticker,
                    defaults={
                        "species": operation.ticket.species,
                        "species_code": operation.ticket.species_code,
                        "ticker": operation.ticket.ticker,
                    },
                )

                reference, _ = await ReferenceModel.get_or_create(
                    detail=operation.reference.detail,
                    defaults={"detail": operation.reference.detail},
                )

                # Now create the operation model with the saved related models
                operation_model = OperationModel(
                    id=operation.id,
                    type_operation=operation_type,
                    ticket=ticket,
                    amount=operation.amount,
                    code=operation.code,
                    accumulated=operation.accumulated,
                    number_receipt=operation.number_receipt,
                    date_liquidation=operation.date_liquidation,
                    date_operation=operation.date_operation,
                    reference=reference,
                    price_of_operation=operation.price_of_operation,
                    import_of_operation=operation.import_of_operation,
                    comprobant_of_operation=operation.comprobant_of_operation,
                )
                operations_records.append(operation_model)
            await OperationModel.bulk_create(operations_records)
            return len(operations_records)

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

        filters: dict[str, Any] = {
            "date_operation__gte": from_date,
            "date_operation__lte": to_date,
        }
        if type_operation:
            pass
            filters["type_operation__type_operation__in"] = [
                op for op in type_operation
            ]

        if ticker:
            filters["ticket__ticker__icontains"] = ticker

        operations_records = (
            await OperationModel.filter(**filters)
            .prefetch_related("type_operation", "ticket", "reference")
            .all()
        )
        return [
            Operation.from_model(operation_record)
            for operation_record in operations_records
        ]

    async def update_operations(
        self,
        properties_to_filter: "OperationProperties",
        properties_to_update: "OperationProperties",
    ) -> int:
        """
        Update operations based on filter criteria.

        Args:
            properties_to_filter: Dictionary with properties to filter operations
            properties_to_update: Dictionary with properties to update

        Returns:
            Number of operations updated
        """

        async with in_transaction():
            # Build filter criteria
            filters: dict[str, Any] = {}

            # Add filter conditions for each provided property
            for key, value in properties_to_filter.items():
                if value is not None:
                    filters[key] = value

            # Validate that at least one filter is provided
            if not filters:
                raise ValueError("At least one filter property must be provided")

            # Find operations matching the filter criteria
            operations_to_update = await OperationModel.filter(**filters).all()

            if not operations_to_update:
                return 0

            # Prepare update data
            update_data: dict[str, Any] = {}

            # Add update values for each provided property
            for key, value in properties_to_update.items():
                if value is not None:
                    update_data[key] = value

            # Validate that at least one update property is provided
            if not update_data:
                raise ValueError("At least one update property must be provided")

            # Update the operations
            updated_count = await OperationModel.filter(**filters).update(**update_data)

            return updated_count

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
        # Validate that at least one parameter is provided
        if not any([id, ticker, type_operation]):
            raise ValueError("At least one parameter must be provided")

        filters: dict[str, Any] = {}

        # Build filters based on provided parameters
        if id is not None:
            filters["id__in"] = list[int](id)

        if ticker is not None:
            filters["ticket__ticker__in"] = ticker

        if type_operation is not None:
            filters["type_operation__type_operation__in"] = [
                op for op in type_operation
            ]

        # Delete operations matching the filters
        deleted_count = await OperationModel.filter(**filters).delete()
        return deleted_count
