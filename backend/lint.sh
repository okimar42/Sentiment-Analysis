#!/bin/bash

# Linting script for Django backend
set -e

echo "🔍 Running linting checks..."

echo "📝 Running Black (code formatting)..."
black --check --diff .

echo "📦 Running isort (import sorting)..."
isort --check-only --diff .

echo "🔍 Running flake8 (style guide enforcement)..."
flake8 .

echo "🔬 Running mypy (type checking)..."
mypy .

echo "✅ All linting checks passed!" 