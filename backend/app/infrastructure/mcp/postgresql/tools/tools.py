"""
PostgreSQL MCP Tools for database schema information and SQL query execution.
Based on postgres-mcp repository implementation patterns.
"""

from typing import Any, Dict, Optional

from app.config.settings import Settings
from app.domain.entities.enums import HBTypeOperations
from app.domain.interfaces.analyzers.strategies.trading_analyzer_strategy_interface import (
    TradingAnalyzerStrategyInterface,
)
from app.domain.interfaces.analyzers.trading_analyzer_interface import (
    TradingAnalyzerInterface,
)
from app.domain.interfaces.repositories.operations_repository_interface import (
    OperationsRepositoryInterface,
)
from app.domain.use_cases.get_positions_use_case import GetPositionsUseCase
from app.infrastructure.analyzers.analyzer_home_broker_data import (
    AnalyzerHomeBrokerData,
)
from app.infrastructure.analyzers.strategies.fifo_strategy import FifoStrategy
from app.infrastructure.db.postgresql.repositories.operations_repository import (
    OperationsRepository,
)
from app.infrastructure.mcp.postgresql.driver.driver import SqlDriver
from fastmcp import FastMCP

_settings = Settings()
_sql_driver: Optional[SqlDriver] = None
_repository: OperationsRepositoryInterface = OperationsRepository()
_strategy: TradingAnalyzerStrategyInterface = FifoStrategy()
_home_broker_analyzer: TradingAnalyzerInterface = AnalyzerHomeBrokerData(
    strategy=_strategy
)


def _get_sql_driver() -> SqlDriver:
    """Get or create the SqlDriver instance."""
    global _sql_driver
    if _sql_driver is None:
        _sql_driver = SqlDriver(engine_url=_settings.POSTGRESQL_URL)
    return _sql_driver


def register_tools(mcp: FastMCP) -> None:
    """
    Register PostgreSQL MCP tools with the FastMCP instance.
    This function should be called after creating the FastMCP instance.
    """

    @mcp.tool()
    async def get_schema_information(
        table_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get database schema information including tables, columns, and constraints.

        Args:
            table_name: Optional table name to filter results. If not provided, returns all tables.

        Returns:
            Dictionary containing schema information with tables, columns, and constraints.
        """
        driver = _get_sql_driver()

        try:
            # Build query based on whether table_name is provided
            if table_name:
                # Get specific table information
                tables_query = """
                    SELECT 
                        t.table_schema,
                        t.table_name,
                        obj_description(c.oid, 'pg_class') as table_comment
                    FROM information_schema.tables t
                    LEFT JOIN pg_class c ON c.relname = t.table_name
                    WHERE t.table_schema NOT IN ('pg_catalog', 'information_schema')
                        AND t.table_type = 'BASE TABLE'
                        AND t.table_name = %s
                    ORDER BY t.table_schema, t.table_name;
                """
                tables_result = await driver.execute_query(
                    tables_query, params=[table_name], force_readonly=True
                )
            else:
                # Get all tables
                tables_query = """
                    SELECT 
                        t.table_schema,
                        t.table_name,
                        obj_description(c.oid, 'pg_class') as table_comment
                    FROM information_schema.tables t
                    LEFT JOIN pg_class c ON c.relname = t.table_name
                    WHERE t.table_schema NOT IN ('pg_catalog', 'information_schema')
                        AND t.table_type = 'BASE TABLE'
                    ORDER BY t.table_schema, t.table_name;
                """
                tables_result = await driver.execute_query(
                    tables_query, force_readonly=True
                )

            if not tables_result:
                return {"tables": [], "message": "No tables found"}

            tables = []
            for table_row in tables_result:
                table_schema = table_row.cells.get("table_schema", "")
                table_name_value = table_row.cells.get("table_name", "")
                table_comment = table_row.cells.get("table_comment")

                # Get columns for this table
                columns_query = """
                    SELECT 
                        column_name,
                        data_type,
                        character_maximum_length,
                        is_nullable,
                        column_default,
                        ordinal_position
                    FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s
                    ORDER BY ordinal_position;
                """
                columns_result = await driver.execute_query(
                    columns_query,
                    params=[table_schema, table_name_value],
                    force_readonly=True,
                )

                columns = []
                if columns_result:
                    for col_row in columns_result:
                        columns.append(
                            {
                                "name": col_row.cells.get("column_name"),
                                "type": col_row.cells.get("data_type"),
                                "max_length": col_row.cells.get(
                                    "character_maximum_length"
                                ),
                                "nullable": col_row.cells.get("is_nullable") == "YES",
                                "default": col_row.cells.get("column_default"),
                                "position": col_row.cells.get("ordinal_position"),
                            }
                        )

                # Get constraints for this table
                constraints_query = """
                    SELECT
                        tc.constraint_name,
                        tc.constraint_type,
                        kcu.column_name,
                        ccu.table_schema AS foreign_table_schema,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints tc
                    LEFT JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                        AND tc.table_schema = kcu.table_schema
                    LEFT JOIN information_schema.constraint_column_usage ccu
                        ON ccu.constraint_name = tc.constraint_name
                        AND ccu.table_schema = tc.table_schema
                    WHERE tc.table_schema = %s AND tc.table_name = %s
                    ORDER BY tc.constraint_type, tc.constraint_name;
                """
                constraints_result = await driver.execute_query(
                    constraints_query,
                    params=[table_schema, table_name_value],
                    force_readonly=True,
                )

                constraints = []
                if constraints_result:
                    for constraint_row in constraints_result:
                        constraint_type = constraint_row.cells.get("constraint_type")
                        constraint_info = {
                            "name": constraint_row.cells.get("constraint_name"),
                            "type": constraint_type,
                            "column": constraint_row.cells.get("column_name"),
                        }

                        # Add foreign key information
                        if constraint_type == "FOREIGN KEY":
                            constraint_info["references"] = {
                                "schema": constraint_row.cells.get(
                                    "foreign_table_schema"
                                ),
                                "table": constraint_row.cells.get("foreign_table_name"),
                                "column": constraint_row.cells.get(
                                    "foreign_column_name"
                                ),
                            }

                        constraints.append(constraint_info)

                tables.append(
                    {
                        "schema": table_schema,
                        "name": table_name_value,
                        "comment": table_comment,
                        "columns": columns,
                        "constraints": constraints,
                    }
                )

            return {"tables": tables}

        except Exception as e:
            return {
                "error": f"Failed to retrieve schema information: {str(e)}",
                "tables": [],
            }

    @mcp.tool()
    async def execute_sql_query(query: str) -> Dict[str, Any]:
        """
        Execute a SQL query against the PostgreSQL database (read-write).

        This tool allows executing any SQL query including SELECT, INSERT, UPDATE, DELETE,
        and DDL statements. Use with caution as it can modify data.

        Args:
            query: SQL query string to execute

        Returns:
            Dictionary containing query results or execution status.
        """
        driver = _get_sql_driver()

        try:
            # Execute the query (read-write mode)
            result = await driver.execute_query(query, force_readonly=False)

            if result is None:
                # DDL or DML statement that doesn't return rows
                return {
                    "success": True,
                    "message": "Query executed successfully",
                    "rows_affected": "unknown",
                    "data": None,
                }

            # Convert RowResult objects to dictionaries
            rows = [row.cells for row in result]

            return {
                "success": True,
                "row_count": len(rows),
                "data": rows,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None,
            }

    @mcp.tool()
    async def get_closed_positions(
        from_date: str,
        to_date: str,
        ticker: str | None = None,
    ) -> Dict[str, Any]:
        """
        Get closed positions from the PostgreSQL database.
        Args:
            from_date: Start date to filter positions. (format: DD/MM/YYYY)
            to_date: End date to filter positions. (format: DD/MM/YYYY)
            ticker: Optional ticker to filter positions. Example: "GGAL"

        Returns:
            Dictionary containing closed positions.
        """
        type_operation = (
            HBTypeOperations.BUY,
            HBTypeOperations.SELL,
            HBTypeOperations.SELL_PARITY,
        )

        get_positions_use_case = GetPositionsUseCase(_repository, _home_broker_analyzer)

        closed_positions = await get_positions_use_case.execute(
            from_date=from_date,
            to_date=to_date,
            type_operation=type_operation,
            ticker=ticker,
        )

        formatted_positions = [
            closed_position.to_formatted_dict() for closed_position in closed_positions
        ]
        return formatted_positions
