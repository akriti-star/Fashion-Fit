#!/bin/bash

# Build script for Vercel
echo "🔨 Building FashionFit for Vercel..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

echo "✅ Build completed successfully!"
