#!/bin/bash
# Railway start script - ensures gunicorn binds to Railway's PORT
# Railway sets PORT environment variable automatically

# Get PORT from environment, Railway sets this automatically
PORT=${PORT:-5000}

echo "🚀 Starting Daiva Anughara application..."
echo "📦 Environment: ${FLASK_ENV:-production}"
echo "🔌 Binding to port: $PORT"
echo "🌐 Host: 0.0.0.0"

# Verify required environment variables
if [ -z "$SQLALCHEMY_DATABASE_URI" ]; then
    echo "⚠️  Warning: SQLALCHEMY_DATABASE_URI not set"
fi

if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  Warning: SECRET_KEY not set - using default (NOT RECOMMENDED FOR PRODUCTION)"
fi

# Start gunicorn with proper configuration
echo "🔄 Starting Gunicorn server..."
exec gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --preload
