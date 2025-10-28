import logging
from datetime import datetime

from fastapi import APIRouter, File, HTTPException, Query, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config.settings import Settings
from app.domain.entities.enums import HBTypeOperations, TypeOfSort
from app.domain.use_cases.delete_positions_use_case import DeletePositionsUseCase
from app.domain.use_cases.get_positions_use_case import GetPositionsUseCase
from app.domain.use_cases.treat_csv_use_case import TreatCsvUseCase
from app.domain.use_cases.update_positions_use_case import UpdatePositionsUseCase
from app.infrastructure.analyzers.analyzer_home_broker_data import (
    AnalyzerHomeBrokerData,
)
from app.infrastructure.analyzers.strategies.fifo_strategy import FifoStrategy
from app.infrastructure.api.schemas import (
    AllPositionsResponse,
    ClosedPositionsResponse,
    DeletePositionsRequest,
    DeletePositionsResponse,
    PaginationInfo,
    UpdatePositionsRequest,
    UpdatePositionsResponse,
    UploadOperationsResponse,
)
from app.infrastructure.db.postgresql.repositories.operations_repository import (
    OperationsRepository,
)
from app.infrastructure.parsers.csv_parser_portfolio import CsvParserPortfolio
from app.infrastructure.parsers.positions_response_parser import PositionsResponseParser


class MainRoutes:
    def __init__(self, limiter=None):
        self.router = APIRouter()
        self.settings = Settings()
        self.logger = logging.getLogger(__name__)

        # Store limiter for use in decorators
        self.limiter = limiter or Limiter(key_func=get_remote_address)

        self.repository = OperationsRepository()
        self.csv_parser = CsvParserPortfolio()
        self.treat_csv_use_case = TreatCsvUseCase(self.repository, self.csv_parser)

        self.fifo_strategy = FifoStrategy()
        self.home_broker_analyzer = AnalyzerHomeBrokerData(self.fifo_strategy)

        self._setup_routes()

    def _validate_pagination(self, offset: int, limit: int) -> None:
        """Validate pagination parameters to prevent performance issues"""
        # Additional validation beyond FastAPI Query constraints
        if offset < 0:
            raise HTTPException(status_code=400, detail="Offset must be non-negative")

        if limit <= 0 or limit > 100:
            raise HTTPException(
                status_code=400, detail="Limit must be between 1 and 100"
            )

        if offset > 10000:
            raise HTTPException(
                status_code=400,
                detail="Offset cannot exceed 10,000 for performance reasons",
            )

        # Prevent potential memory issues with very large result sets
        if offset + limit > 10000:
            raise HTTPException(
                status_code=400,
                detail="Combined offset and limit cannot exceed 10,000 records",
            )

    def _validate_file_upload(self, file: UploadFile) -> None:
        """Validate uploaded file for type, size, and content"""
        # Check file extension
        if not file.filename or not file.filename.lower().endswith(".csv"):
            raise HTTPException(
                status_code=400, detail="File must be a CSV file with .csv extension"
            )

        # Check content type
        if file.content_type not in ["text/csv", "application/csv", "text/plain"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid content type: {file.content_type}. Expected CSV content type",
            )

        # Check file size (10MB limit)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size allowed is {MAX_FILE_SIZE // (1024 * 1024)}MB",
            )

    def _setup_routes(self):
        @self.router.get("/health")
        async def health_check():
            """Health check endpoint - Public access"""
            return {
                "status": "healthy",
                "service": self.settings.APP_NAME,
                "version": self.settings.VERSION,
            }

        @self.router.post("/upload-operations", response_model=UploadOperationsResponse)
        @self.limiter.limit("10/hour")
        async def upload_operations(request: Request, file: UploadFile = File(...)):
            """Upload operations endpoint"""
            try:
                self._validate_file_upload(file)

                operations_created: int = await self.treat_csv_use_case.execute(file)
                return UploadOperationsResponse(
                    message=f"Successfully uploaded {operations_created} operations",
                    status="success",
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Unexpected error in upload_operations: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while processing the file",
                )

        @self.router.get(
            "/closed-positions",
            description="Get only closed position of actions of historical portfolio",
            response_model=ClosedPositionsResponse,
        )
        async def closed_positions(
            from_date: str,
            to_date: str,
            ticker: str | None = Query(
                None,
                regex=r"^[A-Za-z0-9]+$",
                description="Ticker symbol (alphanumeric)",
            ),
            offset: int = Query(
                0, ge=0, le=10000, description="Number of records to skip (max 10,000)"
            ),
            limit: int = Query(
                10,
                ge=1,
                le=100,
                description="Maximum number of records to return (max 100)",
            ),
        ):
            """Get only closed position of actions"""

            try:
                self._validate_pagination(offset, limit)

                type_operation = (
                    HBTypeOperations.BUY,
                    HBTypeOperations.SELL,
                    HBTypeOperations.SELL_PARITY,
                )

                get_positions_use_case = GetPositionsUseCase(
                    self.repository, self.home_broker_analyzer
                )

                closed_positions = await get_positions_use_case.execute(
                    from_date=from_date,
                    to_date=to_date,
                    type_operation=type_operation,
                    ticker=ticker,
                )

                total_count = len(closed_positions)
                paginated_positions = closed_positions[offset : offset + limit]

                formatted_positions = [
                    position.to_formatted_dict() for position in paginated_positions
                ]

                message = self.get_message(len(paginated_positions))

                return ClosedPositionsResponse(
                    message=message,
                    data=formatted_positions,
                    pagination=PaginationInfo(
                        total=total_count,
                        offset=offset,
                        limit=limit,
                        has_more=offset + limit < total_count,
                    ),
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                self.logger.error(f"Unexpected error in closed_positions: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while retrieving closed positions",
                )

        @self.router.get(
            "/all-positions",
            description="Get all positions of actions of historical portfolio",
            response_model=AllPositionsResponse,
        )
        async def all_positions(
            from_date: str,
            to_date: str,
            ticker: str | None = Query(
                None,
                regex=r"^[A-Za-z0-9]+$",
                description="Ticker symbol (alphanumeric)",
            ),
            sort: TypeOfSort = TypeOfSort.ASCENDING,
            offset: int = Query(
                0, ge=0, le=10000, description="Number of records to skip (max 10,000)"
            ),
            limit: int = Query(
                10,
                ge=1,
                le=100,
                description="Maximum number of records to return (max 100)",
            ),
        ):
            """Get all positions of actions"""

            try:
                # Validate pagination parameters
                self._validate_pagination(offset, limit)

                type_operation = (
                    HBTypeOperations.BUY,
                    HBTypeOperations.SELL,
                    HBTypeOperations.SELL_PARITY,
                )

                get_positions_use_case = GetPositionsUseCase(self.repository)

                all_positions = await get_positions_use_case.execute(
                    from_date=from_date,
                    to_date=to_date,
                    type_operation=type_operation,
                    ticker=ticker,
                )

                parser = PositionsResponseParser()
                formatted_positions = parser.parse(all_positions, sort)

                # Apply pagination
                total_count = len(formatted_positions)
                paginated_positions = formatted_positions[offset : offset + limit]

                message = self.get_message(len(paginated_positions))

                return AllPositionsResponse(
                    message=message,
                    data=paginated_positions,
                    pagination=PaginationInfo(
                        total=total_count,
                        offset=offset,
                        limit=limit,
                        has_more=offset + limit < total_count,
                    ),
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                self.logger.error(f"Unexpected error in all_positions: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while retrieving all positions",
                )

        @self.router.delete(
            "/delete-positions",
            description="Delete positions of actions of historical portfolio",
            response_model=DeletePositionsResponse,
        )
        @self.limiter.limit("10/hour")
        async def delete_positions(
            request: Request, delete_request: DeletePositionsRequest
        ):
            """Delete operations based on provided criteria"""

            try:
                delete_operations_use_case = DeletePositionsUseCase(self.repository)

                # Convert list to tuple for type_operations to match use case signature
                type_operations_tuple = (
                    tuple(delete_request.type_operations)
                    if delete_request.type_operations
                    else None
                )

                deleted_count = await delete_operations_use_case.execute(
                    id=delete_request.ids,
                    ticker=delete_request.tickers,
                    type_operation=type_operations_tuple,
                )

                # Enhanced audit logging for delete operation
                self.logger.info(
                    f"DESTRUCTIVE OPERATION - DELETE completed at {datetime.now().isoformat()} - "
                    f"Request: IDs={delete_request.ids}, Tickers={delete_request.tickers}, "
                    f"Type Operations={delete_request.type_operations}, "
                    f"Deleted Count={deleted_count}, "
                    f"Client IP: {get_remote_address(request)}"
                )

                return DeletePositionsResponse(
                    message=f"Successfully deleted {deleted_count} operations",
                    deleted_count=deleted_count,
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                self.logger.error(f"Unexpected error in delete_positions: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while deleting positions",
                )

        @self.router.put(
            "/update-positions",
            description="Update positions of actions of historical portfolio",
            response_model=UpdatePositionsResponse,
        )
        @self.limiter.limit("10/hour")
        async def update_positions(
            request: Request, update_request: UpdatePositionsRequest
        ):
            """Update operations based on provided criteria and update data"""

            try:
                update_operations_use_case = UpdatePositionsUseCase(self.repository)

                updated_count = await update_operations_use_case.execute(
                    properties_to_filter=update_request.to_operation_properties_filter(),
                    properties_to_update=update_request.to_operation_properties_update(),
                )

                # Enhanced audit logging for update operation
                self.logger.info(
                    f"DESTRUCTIVE OPERATION - UPDATE completed at {datetime.now().isoformat()} - "
                    f"Filter Criteria: {update_request.to_operation_properties_filter()}, "
                    f"Update Data: {update_request.to_operation_properties_update()}, "
                    f"Updated Count: {updated_count}, "
                    f"Client IP: {get_remote_address(request)}"
                )

                return UpdatePositionsResponse(
                    message=f"Successfully updated {updated_count} operations",
                    updated_count=updated_count,
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                self.logger.error(f"Unexpected error in update_positions: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while updating positions",
                )

    def get_message(self, count: int) -> str:
        if count == 0:
            return "No records found with the filters provided"
        elif count == 1:
            return "1 record found"
        else:
            return f"{count} records found"
