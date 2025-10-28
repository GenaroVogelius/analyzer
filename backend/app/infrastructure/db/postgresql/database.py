"""
PostgreSQL database utilities for Tortoise ORM.
This module provides utility functions for database operations.
"""

from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError
from app.infrastructure.logger import logger
from app.config.settings import Settings

settings = Settings()


async def connect_to_postgresql():
    """
    Create PostgreSQL database connection using Tortoise ORM.
    This function is kept for backward compatibility with scripts like create_tables.py
    """
    try:
        # Import the config from tortoise_config
        from app.infrastructure.db.postgresql.tortoise_config import TORTOISE_ORM

        # Initialize Tortoise ORM
        await Tortoise.init(config=TORTOISE_ORM)

        # Generate schemas (create tables if they don't exist)
        await Tortoise.generate_schemas()

        logger.info(f"✅ Connected to PostgreSQL at {settings.POSTGRESQL_URL}")

    except DBConnectionError as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: Database connection error - {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
        raise


async def close_postgresql_connection():
    """
    Close PostgreSQL database connection.
    This function is kept for backward compatibility with scripts like create_tables.py
    """
    try:
        await Tortoise.close_connections()
        logger.info("✅ PostgreSQL connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing PostgreSQL connection: {e}")


# Health check function
async def check_postgresql_health() -> bool:
    """Check if PostgreSQL connection is healthy"""
    try:
        # Try to execute a simple query to check connection
        await Tortoise.get_connection("default").execute_query("SELECT 1")
        return True
    except Exception:
        return False
