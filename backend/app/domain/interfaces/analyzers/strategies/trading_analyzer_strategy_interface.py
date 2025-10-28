from abc import abstractmethod
from typing import Protocol, Tuple

from app.domain.entities.entities import Operation, OperationsAnalyzed


class TradingAnalyzerStrategyInterface(Protocol):
    """
    Interface for trading analyzer strategy.
    """

    @abstractmethod
    async def run_strategy(
        self, operations: list[Operation]
    ) -> Tuple[list[OperationsAnalyzed], list[OperationsAnalyzed]]:
        """
        Run the strategy.

        Returns:
            Tuple of (closed_operations, open_operations)
        """
        raise NotImplementedError
