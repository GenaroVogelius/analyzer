from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config.settings import Settings
from app.domain.entities.enums import DatabaseTypes
from app.infrastructure.api.main_routes import MainRoutes
from app.infrastructure.db.main import (
    close_database_connections,
    initialize_databases,
    set_fastapi_app,
)
from app.infrastructure.logger import logger

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Set the FastAPI app instance for database integration
        set_fastapi_app(app)

        # Initialize database connection using the centralized database module
        database_types = [DatabaseTypes.POSTGRESQL]
        await initialize_databases(database_types)

        main_routes = MainRoutes(limiter)
        app.include_router(
            main_routes.router, prefix=settings.API_PREFIX, tags=["api rest"]
        )

        logger.info("Aplicación iniciada correctamente")
        logger.info("Documentación disponible en: http://localhost:8000/docs")
    except Exception as e:
        logger.error(f"Error en startup: {str(e)}")
        raise

    yield

    # Shutdown
    try:
        await close_database_connections(database_types)
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(
        status_code=429, content={"error": "Rate limit exceeded", "status_code": 429}
    ),
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOW_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejo global de errores
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500, content={"error": "Internal server error", "status_code": 500}
    )


if __name__ == "__main__":
    import os

    import uvicorn

    # Usar puerto del debug si está disponible, sino usar 8000
    port = int(os.getenv("DEBUG_PORT", "8001"))

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=port, reload=True, log_level="info"
    )
