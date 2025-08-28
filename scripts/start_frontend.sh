#!/bin/sh
set -e

# ensure env file exists
cp config/.env.example frontend/.env.local

cd frontend
npm run dev
