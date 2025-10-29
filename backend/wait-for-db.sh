#!/bin/bash

set -e

DB_HOST=${POSTGRES_HOST:-postgres}
DB_PORT=${POSTGRES_PORT:-5432}
DB_USER=${POSTGRES_USER:-admin}
DB_NAME=${POSTGRES_DB:-postgresql-backend}

echo "🔄 Waiting for PostgreSQL to be available at $DB_HOST:$DB_PORT..."

wait_for_postgres() {
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "Intento $attempt/$max_attempts: Verificando conexión a PostgreSQL..."
        
        if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" >/dev/null 2>&1; then
            echo "✅ PostgreSQL está disponible!"
            return 0
        fi
        
        echo "⏳ PostgreSQL no está listo aún, esperando 2 segundos..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ Error: PostgreSQL no está disponible después de $max_attempts intentos"
    return 1
}


wait_for_postgres

echo "🔄 Executing migrations..."
uv run aerich upgrade

echo "✅ Migrations completed successfully!"

echo "🚀 Starting FastAPI application..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
