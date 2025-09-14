#!/bin/bash
cd /app/src
exec python -m uvicorn kopi_bot.main:app --host 0.0.0.0 --port ${PORT:-8000}