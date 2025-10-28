from app.domain.entities.entities import Operation, OperationsAnalyzed
from app.domain.interfaces.analyzers.strategies.trading_analyzer_strategy_interface import (
    TradingAnalyzerStrategyInterface,
)
from app.domain.interfaces.analyzers.trading_analyzer_interface import (
    TradingAnalyzerInterface,
)


class AnalyzerHomeBrokerData(TradingAnalyzerInterface):
    """
    Analyze data of dataset which was stored in the data-lake.
    """

    def __init__(self, strategy: TradingAnalyzerStrategyInterface | None):
        self.strategy = strategy

    async def analyze(self, operations: list[Operation]) -> list[OperationsAnalyzed]:
        
        closed_operations, open_operations = await self.strategy.run_strategy(
            operations
        )

        return closed_operations
