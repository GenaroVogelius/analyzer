from datetime import datetime
from typing import Any

from app.domain.entities.enums import HBTypeOperations
from app.domain.interfaces.analyzers.trading_analyzer_interface import (
    TradingAnalyzerInterface,
)
from app.domain.interfaces.repositories.operations_repository_interface import (
    OperationsRepositoryInterface,
)


class GetPositionsUseCase:
    """
    This use case is responsible of getting operations from the database and analyzing them doing business transformation in the middle.
    """

    def __init__(
        self,
        repository: OperationsRepositoryInterface,
        analyzer: TradingAnalyzerInterface | None = None,
    ):
        self.repository = repository
        self.analyzer = analyzer

    async def execute(
        self,
        from_date: str,
        to_date: str,
        type_operation: tuple[HBTypeOperations, ...] | None = None,
        ticker: str | None = None,
    ) -> list[Any]:
        try:
            from_date_parsed = datetime.strptime(from_date, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError(
                f"Invalid date format for 'from_date': '{from_date}'. Expected format: DD/MM/YYYY (e.g., 01/01/2024)"
            )

        try:
            to_date_parsed = datetime.strptime(to_date, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError(
                f"Invalid date format for 'to_date': '{to_date}'. Expected format: DD/MM/YYYY (e.g., 01/01/2024)"
            )

        ticker_parsed = ticker.strip().upper() if ticker else None
        operations = await self.repository.get_operations(
            from_date_parsed,
            to_date_parsed,
            type_operation=type_operation,
            ticker=ticker_parsed,
        )

        if self.analyzer:
            return await self.analyzer.analyze(operations)
        else:
            return operations
