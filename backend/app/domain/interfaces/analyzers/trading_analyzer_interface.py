# app/interfaces/analyzers/trading_analyzer_interface.py
from abc import abstractmethod
from typing import Protocol

from app.domain.entities.entities import Operation, OperationsAnalyzed


class TradingAnalyzerInterface(Protocol):
    """
    Interface for analyzing trading operations data.
    Responsible for processing raw trading data and returning analyzed results.
    """

    @abstractmethod
    async def analyze(self, operations: list[Operation]) -> list[OperationsAnalyzed]:
        """
        Analyzes trading operations from historical data.

        Args:
            operations: List of trading operations to analyze

        Returns:
            List of analyzed trading operations including profits and gains
        """
        raise NotImplementedError("Method analyze must be implemented")
