from app.config.settings import Settings

settings = Settings()

TORTOISE_ORM = {
    "connections": {"default": settings.POSTGRESQL_URL},
    "apps": {
        "models": {
            "models": ["app.infrastructure.db.postgresql.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "timezone": "UTC",
}
