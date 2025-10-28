import datetime

import pytest

from app.domain.entities.entities import Operation, OperationType, Reference, Ticket
from app.domain.entities.enums import HBTypeOperations
from app.infrastructure.analyzers.strategies.fifo_strategy import FifoStrategy
from app.infrastructure.analyzers.strategies.tests.files.mock_operations import (
    mock_operations,
)


@pytest.fixture
def strategy():
    """Fixture that provides a FifoStrategy instance for tests."""
    return FifoStrategy()


@pytest.fixture
def operations():
    """Fixture that provides a list of operations for tests."""
    return mock_operations


class TestFifoStrategy:
    """Test class for FifoStrategy functionality."""

    async def test_run_strategy_with_mock_data(
        self, strategy: FifoStrategy, operations: list[Operation]
    ):
        """Test that the strategy correctly handles the mock operations data."""
        closed_operations, open_operations = await strategy.run_strategy(operations)

        # Filter out invalid operations with amount=0
        valid_closed_operations = [op for op in closed_operations if op.amount > 0]
        valid_open_operations = [op for op in open_operations if op.amount > 0]

        # Should have 3 valid closed operations and 1 valid open operation based on FIFO logic
        assert len(valid_closed_operations) == 3
        assert len(valid_open_operations) == 1

        # Verify closed operations have positive amounts
        for op in valid_closed_operations:
            assert op.amount > 0
            assert op.buy_price > 0
            assert op.sell_price > 0

        # Verify open operations
        for op in valid_open_operations:
            assert op.amount > 0
            assert op.buy_price > 0

    async def test_empty_operations_list(self, strategy: FifoStrategy):
        """Test that the strategy handles empty operations list correctly."""
        closed_operations, open_operations = await strategy.run_strategy([])
        assert len(closed_operations) == 0
        assert len(open_operations) == 0

    async def test_only_buy_operations(self, strategy: FifoStrategy):
        """Test that the strategy handles only buy operations correctly."""
        operations = [
            Operation(
                id=1,
                type_operation=OperationType(type_operation=HBTypeOperations.BUY),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="BUY001",
                accumulated=100.0,
                number_receipt=1001,
                date_liquidation=datetime.date(2024, 1, 15),
                date_operation=datetime.date(2024, 1, 15),
                reference=Reference(detail="Buy AAPL shares"),
                import_of_operation=100.0,
                comprobant_of_operation=1001,
                amount=100.0,
                price_of_operation=1.0,
            ),
            Operation(
                id=2,
                type_operation=OperationType(type_operation=HBTypeOperations.BUY),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="BUY002",
                accumulated=200.0,
                number_receipt=1002,
                date_liquidation=datetime.date(2024, 1, 20),
                date_operation=datetime.date(2024, 1, 20),
                reference=Reference(detail="Buy more AAPL shares"),
                import_of_operation=200.0,
                comprobant_of_operation=1002,
                amount=100.0,
                price_of_operation=2.0,
            ),
        ]

        closed_operations, open_operations = await strategy.run_strategy(operations)
        assert len(closed_operations) == 0
        assert len(open_operations) == 2

    async def test_only_sell_operations(self, strategy: FifoStrategy):
        """Test that the strategy handles only sell operations correctly."""
        operations = [
            Operation(
                id=1,
                type_operation=OperationType(type_operation=HBTypeOperations.SELL),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="SELL001",
                accumulated=100.0,
                number_receipt=2001,
                date_liquidation=datetime.date(2024, 2, 15),
                date_operation=datetime.date(2024, 2, 15),
                reference=Reference(detail="Sell AAPL shares"),
                import_of_operation=100.0,
                comprobant_of_operation=2001,
                amount=100.0,
                price_of_operation=2.0,
            ),
        ]

        closed_operations, open_operations = await strategy.run_strategy(operations)
        assert len(closed_operations) == 0
        assert len(open_operations) == 0

    async def test_perfect_match_scenario(self, strategy: FifoStrategy):
        """Test FIFO with perfect buy/sell matches."""
        operations = [
            # Buy 100 shares at $1.0
            Operation(
                id=1,
                type_operation=OperationType(type_operation=HBTypeOperations.BUY),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="BUY001",
                accumulated=100.0,
                number_receipt=1001,
                date_liquidation=datetime.date(2024, 1, 15),
                date_operation=datetime.date(2024, 1, 15),
                reference=Reference(detail="Buy AAPL shares"),
                import_of_operation=100.0,
                comprobant_of_operation=1001,
                amount=100.0,
                price_of_operation=1.0,
            ),
            # Sell 100 shares at $2.0
            Operation(
                id=2,
                type_operation=OperationType(type_operation=HBTypeOperations.SELL),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="SELL001",
                accumulated=0.0,
                number_receipt=2001,
                date_liquidation=datetime.date(2024, 2, 15),
                date_operation=datetime.date(2024, 2, 15),
                reference=Reference(detail="Sell AAPL shares"),
                import_of_operation=200.0,
                comprobant_of_operation=2001,
                amount=100.0,
                price_of_operation=2.0,
            ),
        ]

        closed_operations, open_operations = await strategy.run_strategy(operations)
        assert len(closed_operations) == 1
        assert len(open_operations) == 0

        closed_op = closed_operations[0]
        assert closed_op.ticker == "AAPL"
        assert closed_op.amount == 100
        assert closed_op.buy_price == 1.0
        assert closed_op.sell_price == 2.0
        assert closed_op.nominal_gain == 100.0  # (2.0 - 1.0) * 100

    async def test_partial_sell_scenario(self, strategy: FifoStrategy):
        """Test FIFO with partial sell (sell less than buy)."""
        operations = [
            # Buy 200 shares at $1.0
            Operation(
                id=1,
                type_operation=OperationType(type_operation=HBTypeOperations.BUY),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="BUY001",
                accumulated=200.0,
                number_receipt=1001,
                date_liquidation=datetime.date(2024, 1, 15),
                date_operation=datetime.date(2024, 1, 15),
                reference=Reference(detail="Buy AAPL shares"),
                import_of_operation=200.0,
                comprobant_of_operation=1001,
                amount=200.0,
                price_of_operation=1.0,
            ),
            # Sell 100 shares at $2.0
            Operation(
                id=2,
                type_operation=OperationType(type_operation=HBTypeOperations.SELL),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="SELL001",
                accumulated=100.0,
                number_receipt=2001,
                date_liquidation=datetime.date(2024, 2, 15),
                date_operation=datetime.date(2024, 2, 15),
                reference=Reference(detail="Sell AAPL shares"),
                import_of_operation=200.0,
                comprobant_of_operation=2001,
                amount=100.0,
                price_of_operation=2.0,
            ),
        ]

        closed_operations, open_operations = await strategy.run_strategy(operations)
        assert len(closed_operations) == 1
        assert len(open_operations) == 1

        # Closed operation: 100 shares sold
        closed_op = closed_operations[0]
        assert closed_op.amount == 100
        assert closed_op.buy_price == 1.0
        assert closed_op.sell_price == 2.0

        # Open operation: 100 shares remaining
        open_op = open_operations[0]
        assert open_op.amount == 100
        assert open_op.buy_price == 1.0

    async def test_multiple_buys_single_sell(self, strategy: FifoStrategy):
        """Test FIFO with multiple buys and single sell."""
        operations = [
            # Buy 100 shares at $1.0
            Operation(
                id=1,
                type_operation=OperationType(type_operation=HBTypeOperations.BUY),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="BUY001",
                accumulated=100.0,
                number_receipt=1001,
                date_liquidation=datetime.date(2024, 1, 15),
                date_operation=datetime.date(2024, 1, 15),
                reference=Reference(detail="Buy AAPL shares"),
                import_of_operation=100.0,
                comprobant_of_operation=1001,
                amount=100.0,
                price_of_operation=1.0,
            ),
            # Buy 100 shares at $2.0
            Operation(
                id=2,
                type_operation=OperationType(type_operation=HBTypeOperations.BUY),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="BUY002",
                accumulated=200.0,
                number_receipt=1002,
                date_liquidation=datetime.date(2024, 1, 20),
                date_operation=datetime.date(2024, 1, 20),
                reference=Reference(detail="Buy more AAPL shares"),
                import_of_operation=200.0,
                comprobant_of_operation=1002,
                amount=100.0,
                price_of_operation=2.0,
            ),
            # Sell 150 shares at $3.0
            Operation(
                id=3,
                type_operation=OperationType(type_operation=HBTypeOperations.SELL),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="SELL001",
                accumulated=50.0,
                number_receipt=2001,
                date_liquidation=datetime.date(2024, 2, 15),
                date_operation=datetime.date(2024, 2, 15),
                reference=Reference(detail="Sell AAPL shares"),
                import_of_operation=450.0,
                comprobant_of_operation=2001,
                amount=150.0,
                price_of_operation=3.0,
            ),
        ]

        closed_operations, open_operations = await strategy.run_strategy(operations)

        # Filter out invalid operations with amount=0
        valid_closed_operations = [op for op in closed_operations if op.amount > 0]
        valid_open_operations = [op for op in open_operations if op.amount > 0]

        assert len(valid_closed_operations) == 2
        assert len(valid_open_operations) == 1

        # First closed operation: 100 shares from second buy (processed first due to reverse order)
        closed_op1 = valid_closed_operations[0]
        assert closed_op1.amount == 100
        assert closed_op1.buy_price == 2.0  # Second buy price
        assert closed_op1.sell_price == 3.0

        # Second closed operation: 50 shares from first buy
        closed_op2 = valid_closed_operations[1]
        assert closed_op2.amount == 50
        assert closed_op2.buy_price == 1.0  # First buy price
        assert closed_op2.sell_price == 3.0

        # Open operation: 50 shares remaining from first buy
        open_op = valid_open_operations[0]
        assert open_op.amount == 50
        assert open_op.buy_price == 1.0

    async def test_non_trading_operations_ignored(self, strategy: FifoStrategy):
        """Test that non-trading operations (dividends, receipts, etc.) are ignored."""
        operations = [
            Operation(
                id=1,
                type_operation=OperationType(type_operation=HBTypeOperations.DIVIDEND),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="DIV001",
                accumulated=0.0,
                number_receipt=3001,
                date_liquidation=datetime.date(2024, 3, 1),
                date_operation=datetime.date(2024, 3, 1),
                reference=Reference(detail="AAPL dividend payment"),
                import_of_operation=10.0,
                comprobant_of_operation=3001,
                amount=0.0,
                price_of_operation=None,
            ),
            Operation(
                id=2,
                type_operation=OperationType(type_operation=HBTypeOperations.RECEIPT),
                ticket=Ticket(species="CASH", species_code="CASH", ticker="CASH"),
                code="REC001",
                accumulated=0.0,
                number_receipt=3002,
                date_liquidation=datetime.date(2024, 3, 5),
                date_operation=datetime.date(2024, 3, 5),
                reference=Reference(detail="Cash receipt"),
                import_of_operation=1000.0,
                comprobant_of_operation=3002,
                amount=0.0,
                price_of_operation=None,
            ),
        ]

        closed_operations, open_operations = await strategy.run_strategy(operations)
        assert len(closed_operations) == 0
        assert len(open_operations) == 0

    async def test_different_tickers_separate(self, strategy: FifoStrategy):
        """Test that different tickers are handled separately."""
        operations = [
            # AAPL buy
            Operation(
                id=1,
                type_operation=OperationType(type_operation=HBTypeOperations.BUY),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="BUY001",
                accumulated=100.0,
                number_receipt=1001,
                date_liquidation=datetime.date(2024, 1, 15),
                date_operation=datetime.date(2024, 1, 15),
                reference=Reference(detail="Buy AAPL shares"),
                import_of_operation=100.0,
                comprobant_of_operation=1001,
                amount=100.0,
                price_of_operation=1.0,
            ),
            # MSFT buy
            Operation(
                id=2,
                type_operation=OperationType(type_operation=HBTypeOperations.BUY),
                ticket=Ticket(species="MSFT", species_code="MSFT", ticker="MSFT"),
                code="BUY002",
                accumulated=50.0,
                number_receipt=1002,
                date_liquidation=datetime.date(2024, 1, 20),
                date_operation=datetime.date(2024, 1, 20),
                reference=Reference(detail="Buy MSFT shares"),
                import_of_operation=50.0,
                comprobant_of_operation=1002,
                amount=50.0,
                price_of_operation=2.0,
            ),
            # AAPL sell
            Operation(
                id=3,
                type_operation=OperationType(type_operation=HBTypeOperations.SELL),
                ticket=Ticket(species="AAPL", species_code="AAPL", ticker="AAPL"),
                code="SELL001",
                accumulated=0.0,
                number_receipt=2001,
                date_liquidation=datetime.date(2024, 2, 15),
                date_operation=datetime.date(2024, 2, 15),
                reference=Reference(detail="Sell AAPL shares"),
                import_of_operation=200.0,
                comprobant_of_operation=2001,
                amount=100.0,
                price_of_operation=3.0,
            ),
        ]

        closed_operations, open_operations = await strategy.run_strategy(operations)
        assert len(closed_operations) == 1
        assert len(open_operations) == 1

        # Closed operation should be AAPL
        closed_op = closed_operations[0]
        assert closed_op.ticker == "AAPL"

        # Open operation should be MSFT
        open_op = open_operations[0]
        assert open_op.ticker == "MSFT"
