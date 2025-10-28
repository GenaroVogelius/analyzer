from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel

from app.domain.entities.entities import Operation
from app.domain.entities.enums import TypeOfSort
from app.domain.interfaces.parsers.response_parser_interface import (
    ResponseParserInterface,
)


class PositionResponse(BaseModel):
    id: int
    type_operation: str
    ticket: str
    species: str
    reference: str
    amount: float
    code: str
    accumulated: float
    number_receipt: int
    date_liquidation: str
    date_operation: str


class PositionsResponseParser(ResponseParserInterface):
    """
    Parser for positions API response data.
    Flattens nested structures into a single level dictionary.
    """

    def parse(
        self, positions: List[Operation], sort: TypeOfSort = TypeOfSort.ASCENDING
    ) -> List[Dict[str, Any]]:
        """
        Parse a list of Operation entities and convert them to PositionResponse dictionaries.

        Args:
            positions: List of Operation entities
            sort: Type of sorting to apply (default: ASCENDING)

        Returns:
            List of PositionResponse dictionaries sorted by date_operation
        """
        position_responses = []

        for operation in positions:
            position_response = self._convert_operation_to_position_response(operation)
            position_responses.append(position_response.dict())

        # Sort by date_operation (newest first by default), then by date_liquidation as secondary sort
        def parse_date(date_str: str) -> datetime:
            """Parse DD/MM/YYYY date string to datetime object for proper sorting."""
            return datetime.strptime(date_str, "%d/%m/%Y")

        def sort_key(x: Dict[str, Any]) -> tuple:
            """Create a tuple for multi-level sorting: (date_operation, date_liquidation)."""
            return (parse_date(x["date_operation"]), parse_date(x["date_liquidation"]))

        if sort == TypeOfSort.ASCENDING:
            position_responses.sort(key=sort_key, reverse=False)
        else:  # DESCENDING
            position_responses.sort(key=sort_key, reverse=True)

        return position_responses

    def _convert_operation_to_position_response(
        self, operation: Operation
    ) -> PositionResponse:
        """
        Convert a single Operation to PositionResponse.

        Args:
            operation: The Operation to convert

        Returns:
            PositionResponse entity
        """
        return PositionResponse(
            id=operation.id,
            type_operation=operation.type_operation.type_operation,
            ticket=operation.ticket.ticker or "UNKNOWN",
            species=operation.ticket.species,
            reference=operation.reference.detail or "",
            amount=operation.amount or 0.0,
            code=operation.code,
            accumulated=operation.accumulated,
            number_receipt=operation.number_receipt,
            date_liquidation=operation.date_liquidation.strftime("%d/%m/%Y"),
            date_operation=operation.date_operation.strftime("%d/%m/%Y"),
        )
