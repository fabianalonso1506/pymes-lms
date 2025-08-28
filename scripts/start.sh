#!/bin/bash
set -e

# copy env file for backend and frontend
cp config/.env.example .env
cp config/.env.example frontend/.env.local

# wait for postgres
until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
  echo "Waiting for Postgres..."
  sleep 1
done

# run migrations
alembic -c backend/alembic.ini upgrade head

# seed database
python scripts/seed/seed.py

# start backend server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
