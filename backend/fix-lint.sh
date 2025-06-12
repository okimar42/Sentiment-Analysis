#!/bin/bash

# Comprehensive linting fix script for Django backend
set -e

echo "🔧 Running comprehensive linting fixes..."

echo "🗑️  Removing unused imports..."
autoflake --remove-all-unused-imports --recursive --in-place .

echo "📝 Running Black (code formatting)..."
black .

echo "📦 Running isort (import sorting)..."
isort .

echo "✅ Linting fixes complete!" 