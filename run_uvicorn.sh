#!/bin/bash

# Apply Alembic migrations
echo "Applying database migrations..."
alembic upgrade head

# Start uvicorn server
echo "Starting uvicorn server..."
uvicorn PhotoShare.main:app --host 0.0.0.0 --port 8000
