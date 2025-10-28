import io
import math
import os
from typing import Union, get_args, get_origin, get_type_hints
from unittest.mock import Mock

import pytest

from app.domain.entities.entities import Operation
from app.infrastructure.parsers.csv_parser_portfolio import CsvParserPortfolio


@pytest.fixture
def parser():
    """Fixture that provides a CsvParser instance for tests."""
    return CsvParserPortfolio()


@pytest.fixture
def csv_file_path():
    """Fixture that provides the path to the test CSV file."""
    return os.path.join(os.path.dirname(__file__), "files", "historical_portfolio.csv")


@pytest.fixture
def mock_upload_file(csv_file_path):
    """Fixture that creates a mock UploadFile from the actual CSV file."""
    with open(csv_file_path, "rb") as f:
        file_content = f.read()

    mock_file = Mock()
    mock_file.file = io.BytesIO(file_content)
    mock_file.filename = "historical_portfolio.csv"
    mock_file.content_type = "text/csv"

    return mock_file


def _validate_type_annotation(instance, expected_type):
    """Helper function to validate that an instance matches the expected type annotation."""
    if expected_type is type(None):
        return instance is None

    # Handle Union types (e.g., float | None)
    origin = get_origin(expected_type)
    if origin is Union:
        args = get_args(expected_type)
        return any(_validate_type_annotation(instance, arg) for arg in args)

    # Handle direct type matching
    return isinstance(instance, expected_type)


class TestCsvParserPortfolio:
    """Test class for CsvParser functionality."""

    def test_parse(self, parser, mock_upload_file):
        """Test that the parser correctly handles the structure of the actual CSV file."""
        operations = parser.parse(mock_upload_file)

        assert len(operations) == 341

        # Test that all operations have the correct structure using domain types
        operation_hints = get_type_hints(Operation)

        for operation in operations:
            # Validate the operation instance itself
            assert isinstance(operation, Operation)

            # Validate each field using the domain type annotations
            for field_name, expected_type in operation_hints.items():
                field_value = getattr(operation, field_name)
                assert _validate_type_annotation(field_value, expected_type), (
                    f"Field '{field_name}' has incorrect type. Expected {expected_type}, got {type(field_value)}"
                )

        operation_types = {op.type_operation.type_operation for op in operations}
        assert len(operation_types) == 21

        
        tickers = {op.ticket.ticker for op in operations}
        assert len(tickers) == 34

        # Test that there are no nan values in the parsed data
        for operation in operations:
            # Check that no numeric fields contain nan
            if operation.amount is not None:
                assert not math.isnan(operation.amount)
            assert not (
                isinstance(operation.accumulated, float)
                and math.isnan(operation.accumulated)
            )

            # Check that string fields don't contain nan
            assert operation.type_operation.type_operation is not None
            assert not (
                isinstance(operation.type_operation.type_operation, float)
                and math.isnan(operation.type_operation.type_operation)
            )

            # Check that reference detail doesn't contain nan
            if operation.reference.detail is not None:
                assert not (
                    isinstance(operation.reference.detail, float)
                    and math.isnan(operation.reference.detail)
                )
