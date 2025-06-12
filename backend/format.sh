#!/bin/bash

# Auto-formatting script for Django backend
set -e

echo "🔧 Running auto-formatting..."

echo "📝 Running Black (code formatting)..."
black .

echo "📦 Running isort (import sorting)..."
isort .

echo "✅ Auto-formatting complete!" 