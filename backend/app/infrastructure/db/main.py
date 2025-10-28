"""
Database initialization module.
This module provides database-agnostic initialization functions.
"""

from app.config.settings import Settings
from app.domain.entities.enums import DatabaseTypes
from app.infrastructure.logger import logger

settings = Settings()

# Global variable to store the FastAPI app for Tortoise ORM integration
_fastapi_app = None


def set_fastapi_app(app):
    """
    Set the FastAPI app instance for Tortoise ORM integration.
    This should be called from the main FastAPI application.
    """
    global _fastapi_app
    _fastapi_app = app


async def initialize_databases(db_types: list[DatabaseTypes]):
    """
    Initialize database connection based on configuration.
    This function is database-agnostic and will use the configured database type.
    """
    try:
        if DatabaseTypes.POSTGRESQL in db_types:
            # Initialize Tortoise ORM directly for reliable startup
            from app.infrastructure.db.postgresql.database import connect_to_postgresql

            await connect_to_postgresql()
            logger.info("PostgreSQL connection established")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


async def close_database_connections(db_types: list[DatabaseTypes]):
    """
    Close database connection based on configuration.
    This function is database-agnostic and will use the configured database type.
    Note: PostgreSQL is now handled by RegisterTortoise in FastAPI main.py
    """
    try:

        if DatabaseTypes.POSTGRESQL in db_types:
            # PostgreSQL cleanup
            from app.infrastructure.db.postgresql.database import (
                close_postgresql_connection,
            )

            await close_postgresql_connection()
            logger.info("PostgreSQL connection closed")

    except Exception as e:
        logger.error(f"Error closing database connection: {str(e)}")
        raise
