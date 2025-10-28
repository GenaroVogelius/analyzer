from datetime import date, datetime
from typing import Any, List, cast

from pydantic import BaseModel, Field

from app.domain.entities.enums import HBTypeOperations


class OperationTypeResponse(BaseModel):
    type_operation: str


class TicketResponse(BaseModel):
    species: str
    species_code: str
    ticker: str


class ReferenceResponse(BaseModel):
    detail: str | None = None


class OperationResponse(BaseModel):
    id: int
    type_operation: OperationTypeResponse
    ticket: TicketResponse
    amount: int
    code: str
    accumulated: str
    number_receipt: str
    date_liquidation: datetime
    date_operation: datetime
    reference: ReferenceResponse


class UploadOperationsResponse(BaseModel):
    message: str
    status: str


class DeletePositionsRequest(BaseModel):
    """Request model for deleting positions"""

    ids: List[int] | None = Field(None, description="List of operation IDs to delete")
    tickers: List[str] | None = Field(
        None, description="List of tickers to delete operations for"
    )
    type_operations: List[HBTypeOperations] | None = Field(
        None, description="List of operation types to delete"
    )

    def model_post_init(self, __context) -> None:
        """Validate that at least one parameter is provided"""
        if not any([self.ids, self.tickers, self.type_operations]):
            raise ValueError(
                "At least one parameter (ids, tickers, or type_operations) must be provided"
            )


class DeletePositionsResponse(BaseModel):
    """Response model for delete operations"""

    message: str
    deleted_count: int


class UpdatePositionsRequest(BaseModel):
    """Request model for updating positions"""

    # Filter criteria fields
    filter_id: int | None = Field(None, description="Filter by operation ID")
    filter_code: str | None = Field(None, description="Filter by code")
    filter_accumulated: float | None = Field(
        None, description="Filter by accumulated value"
    )
    filter_number_receipt: int | None = Field(
        None, description="Filter by receipt number"
    )
    filter_date_liquidation: date | None = Field(
        None, description="Filter by liquidation date"
    )
    filter_date_operation: date | None = Field(
        None, description="Filter by operation date"
    )
    filter_import_of_operation: float | None = Field(
        None, description="Filter by import of operation"
    )
    filter_comprobant_of_operation: int | None = Field(
        None, description="Filter by comprobant of operation"
    )
    filter_amount: float | None = Field(None, description="Filter by amount")
    filter_price_of_operation: float | None = Field(
        None, description="Filter by price of operation"
    )

    # Update data fields
    update_code: str | None = Field(None, description="Update code")
    update_accumulated: float | None = Field(
        None, description="Update accumulated value"
    )
    update_number_receipt: int | None = Field(None, description="Update receipt number")
    update_date_liquidation: date | None = Field(
        None, description="Update liquidation date"
    )
    update_date_operation: date | None = Field(
        None, description="Update operation date"
    )
    update_import_of_operation: float | None = Field(
        None, description="Update import of operation"
    )
    update_comprobant_of_operation: int | None = Field(
        None, description="Update comprobant of operation"
    )
    update_amount: float | None = Field(None, description="Update amount")
    update_price_of_operation: float | None = Field(
        None, description="Update price of operation"
    )

    def model_post_init(self, __context) -> None:
        """Validate that at least one filter and one update field is provided"""
        filter_fields = [
            self.filter_id,
            self.filter_code,
            self.filter_accumulated,
            self.filter_number_receipt,
            self.filter_date_liquidation,
            self.filter_date_operation,
            self.filter_import_of_operation,
            self.filter_comprobant_of_operation,
            self.filter_amount,
            self.filter_price_of_operation,
        ]
        update_fields = [
            self.update_code,
            self.update_accumulated,
            self.update_number_receipt,
            self.update_date_liquidation,
            self.update_date_operation,
            self.update_import_of_operation,
            self.update_comprobant_of_operation,
            self.update_amount,
            self.update_price_of_operation,
        ]

        if not any(filter_fields):
            raise ValueError("At least one filter criteria must be provided")
        if not any(update_fields):
            raise ValueError("At least one update field must be provided")

    def to_operation_properties_filter(self):
        """Convert to OperationProperties for filtering"""
        from app.domain.interfaces.repositories.operations_repository_interface import (
            OperationProperties,
        )

        filter_dict = {}
        if self.filter_id is not None:
            filter_dict["id"] = self.filter_id
        if self.filter_code is not None:
            filter_dict["code"] = self.filter_code
        if self.filter_accumulated is not None:
            filter_dict["accumulated"] = self.filter_accumulated
        if self.filter_number_receipt is not None:
            filter_dict["number_receipt"] = self.filter_number_receipt
        if self.filter_date_liquidation is not None:
            filter_dict["date_liquidation"] = self.filter_date_liquidation
        if self.filter_date_operation is not None:
            filter_dict["date_operation"] = self.filter_date_operation
        if self.filter_import_of_operation is not None:
            filter_dict["import_of_operation"] = self.filter_import_of_operation
        if self.filter_comprobant_of_operation is not None:
            filter_dict["comprobant_of_operation"] = self.filter_comprobant_of_operation
        if self.filter_amount is not None:
            filter_dict["amount"] = self.filter_amount
        if self.filter_price_of_operation is not None:
            filter_dict["price_of_operation"] = self.filter_price_of_operation

        return cast(OperationProperties, filter_dict)

    def to_operation_properties_update(self):
        """Convert to OperationProperties for updating"""
        from app.domain.interfaces.repositories.operations_repository_interface import (
            OperationProperties,
        )

        update_dict = {}
        if self.update_code is not None:
            update_dict["code"] = self.update_code
        if self.update_accumulated is not None:
            update_dict["accumulated"] = self.update_accumulated
        if self.update_number_receipt is not None:
            update_dict["number_receipt"] = self.update_number_receipt
        if self.update_date_liquidation is not None:
            update_dict["date_liquidation"] = self.update_date_liquidation
        if self.update_date_operation is not None:
            update_dict["date_operation"] = self.update_date_operation
        if self.update_import_of_operation is not None:
            update_dict["import_of_operation"] = self.update_import_of_operation
        if self.update_comprobant_of_operation is not None:
            update_dict["comprobant_of_operation"] = self.update_comprobant_of_operation
        if self.update_amount is not None:
            update_dict["amount"] = self.update_amount
        if self.update_price_of_operation is not None:
            update_dict["price_of_operation"] = self.update_price_of_operation

        return cast(OperationProperties, update_dict)


class UpdatePositionsResponse(BaseModel):
    """Response model for update operations"""

    message: str
    updated_count: int


class PaginationInfo(BaseModel):
    """Pagination information"""

    total: int
    offset: int
    limit: int
    has_more: bool


class ClosedPositionsResponse(BaseModel):
    """Response model for closed positions"""

    message: str
    data: List[Any]
    pagination: PaginationInfo


class AllPositionsResponse(BaseModel):
    """Response model for all positions"""

    message: str
    data: List[Any]
    pagination: PaginationInfo
