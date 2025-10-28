import datetime

import pandas as pd

from app.domain.entities.entities import Operation, OperationsAnalyzed
from app.domain.entities.enums import (
    DatabaseColumnsOperations,
    HBTypeOperations,
    OperationsAnalyzedColumns,
)
from app.domain.interfaces.analyzers.strategies.trading_analyzer_strategy_interface import (
    TradingAnalyzerStrategyInterface,
)
from app.infrastructure.utils.formulas.formulas import (
    calculate_nominal_profit,
    calculate_percentage_gain,
    calculate_tna,
)


class FifoStrategy(TradingAnalyzerStrategyInterface):
    """
    Strategy for analyzing trading operations using First In First Out (FIFO) strategy.
    """

    def __init__(self):
        self._id_counter = 0

    async def run_strategy(
        self, operations: list[Operation]
    ) -> tuple[list[OperationsAnalyzed], list[OperationsAnalyzed]]:
        """
        Match buy operations with sell operations using First In First Out (FIFO) strategy.
        Returns both closed operations (those with both buy and sell) and open operations (unmatched buys).

        Returns:
            Tuple of (closed_operations, open_operations)
        """
        # Convert Operation dataclasses to DataFrame with flat structure
        df = self._convert_operations_to_dataframe(operations)

        # Check if DataFrame is empty or doesn't have required columns
        if df.empty:
            return [], []

        df = df[::-1]
        df[DatabaseColumnsOperations.AMOUNT] = df[
            DatabaseColumnsOperations.AMOUNT
        ].abs()

        closed_operations = []
        open_operations = []

        # Track remaining amounts for each operation
        remaining_amounts = df[OperationsAnalyzedColumns.AMOUNT].copy()

        # Iterate through all operations chronologically
        for buy_index, buy_row in df.iterrows():
            if (
                buy_row[DatabaseColumnsOperations.TYPE_OPERATION]
                == HBTypeOperations.BUY
                and remaining_amounts[buy_index] > 0
            ):
                buy_ticket = buy_row[DatabaseColumnsOperations.TICKER]
                buy_price = buy_row[DatabaseColumnsOperations.PRICE]
                buy_date = pd.to_datetime(
                    buy_row[DatabaseColumnsOperations.DATE_OPERATION]
                )
                buy_amount = remaining_amounts[buy_index]

                # Find matching sell operations for the same ticker after buy date
                sell_condition = (
                    (df[DatabaseColumnsOperations.TICKER] == buy_ticket)
                    & (
                        df[DatabaseColumnsOperations.TYPE_OPERATION].isin(
                            [HBTypeOperations.SELL, HBTypeOperations.SELL_PARITY]
                        )
                    )
                    & (
                        pd.to_datetime(df[DatabaseColumnsOperations.DATE_OPERATION])
                        >= buy_date
                    )
                )

                sell_matches = df[sell_condition]

                # If no sell matches, create open position
                if sell_matches.empty:
                    open_operation = self._create_operations_analyzed(
                        buy_date=buy_date,
                        sell_date=datetime.datetime.today(),
                        buy_price=buy_price,
                        sell_price=buy_price,  # Use buy price as placeholder for open positions
                        amount=buy_amount,
                        ticket=buy_ticket,
                    )
                    open_operations.append(open_operation)
                    remaining_amounts[buy_index] = 0
                    continue

                # Process each sell match
                for sell_index, sell_row in sell_matches.iterrows():
                    if remaining_amounts[buy_index] <= 0:
                        break
                    sell_amount = remaining_amounts[sell_index]
                    sell_price = sell_row[DatabaseColumnsOperations.PRICE]
                    sell_date = datetime.datetime.combine(
                        sell_row[DatabaseColumnsOperations.DATE_OPERATION],
                        datetime.time(),
                    )

                    # There is a remainder of buy
                    if buy_amount > sell_amount:
                        # Create closed operation for the sell amount
                        closed_operation = self._create_operations_analyzed(
                            buy_date=buy_date,
                            sell_date=sell_date,
                            buy_price=buy_price,
                            sell_price=sell_price,
                            amount=sell_amount,
                            ticket=buy_ticket,
                        )
                        closed_operations.append(closed_operation)

                        # Update remaining amounts
                        remaining_amounts[buy_index] -= sell_amount
                        remaining_amounts[sell_index] = 0
                        buy_amount -= sell_amount

                    # There is a remainder of sell or the position is closed
                    elif buy_amount <= sell_amount:
                        # Create closed operation for the buy amount

                        closed_operation = self._create_operations_analyzed(
                            buy_date=buy_date,
                            sell_date=sell_date,
                            buy_price=buy_price,
                            sell_price=sell_price,
                            amount=buy_amount,
                            ticket=buy_ticket,
                        )
                        closed_operations.append(closed_operation)

                        # Update remaining amounts
                        remaining_amounts[sell_index] -= buy_amount
                        remaining_amounts[buy_index] = 0
                        buy_amount = 0
                        break

                # If there's still a remainder of buy_amount after processing all sells,
                # create an open position for the remaining amount
                if buy_amount > 0:
                    # Check if there are any future sells that could close this position
                    future_sells_condition = (
                        (df[DatabaseColumnsOperations.TICKER] == buy_ticket)
                        & (
                            df[DatabaseColumnsOperations.TYPE_OPERATION].isin(
                                [HBTypeOperations.SELL, HBTypeOperations.SELL_PARITY]
                            )
                        )
                        & (
                            buy_date.date()
                            < df[DatabaseColumnsOperations.DATE_OPERATION]
                        )
                        & (remaining_amounts > 0)
                    )
                    future_sells_df = df[future_sells_condition]

                    # Only create open position if there are no future sells at all
                    if future_sells_df.empty:
                        open_operation = self._create_operations_analyzed(
                            buy_date=buy_date,
                            sell_date=datetime.datetime.today(),
                            buy_price=buy_price,
                            sell_price=buy_price,  # Use buy price as placeholder for open positions
                            amount=buy_amount,
                            ticket=buy_ticket,
                        )
                        open_operations.append(open_operation)

        return closed_operations, open_operations

    def _convert_operations_to_dataframe(
        self, operations: list[Operation]
    ) -> pd.DataFrame:
        """
        Convert Operation dataclasses to DataFrame with flat structure and calculated prices.
        """
        data = []
        for operation in operations:
            # Calculate price from accumulated/amount
            data.append(
                {
                    DatabaseColumnsOperations.TYPE_OPERATION: operation.type_operation.type_operation,
                    DatabaseColumnsOperations.TICKER: operation.ticket.ticker,
                    DatabaseColumnsOperations.AMOUNT: operation.amount or 0,
                    DatabaseColumnsOperations.PRICE: operation.price_of_operation,
                    DatabaseColumnsOperations.DATE_OPERATION: operation.date_operation,
                    DatabaseColumnsOperations.DATE_LIQUIDATION: operation.date_liquidation,
                    DatabaseColumnsOperations.ACCUMULATED: operation.accumulated,
                }
            )

        return pd.DataFrame(data)

    def _create_operations_analyzed(
        self,
        buy_date: datetime.datetime,
        sell_date: datetime.datetime,
        buy_price: float,
        sell_price: float,
        amount: float,
        ticket: str,
    ) -> OperationsAnalyzed:
        """
        Create OperationsAnalyzed dataclass instance from matched operations.
        """
        # Calculate time difference in days
        time_diff = (sell_date - buy_date).days
        t = time_diff if time_diff > 0 else 1

        # Calculate amounts
        inverted_amount = amount * buy_price
        current_amount = amount * sell_price

        # Calculate gains
        nominal_gain = calculate_nominal_profit(buy_price, sell_price, int(amount))
        percentage_gain = calculate_percentage_gain(buy_price, sell_price)
        tna = calculate_tna(buy_price, sell_price, int(t))

        self._id_counter += 1
        return OperationsAnalyzed(
            id=self._id_counter,
            ticker=ticket,
            amount=int(amount),
            date_operation=buy_date,
            date_liquidation=sell_date,
            buy_price=buy_price,
            sell_price=sell_price,
            inverted_amount=inverted_amount,
            current_amount=current_amount,
            percentage_gain=percentage_gain,
            nominal_gain=nominal_gain,
            tna=tna,
        )
