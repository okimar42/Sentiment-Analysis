#!/bin/bash

# Generate comprehensive linting summary report
echo "📊 Backend Linting Summary Report"
echo "================================="
echo

echo "🔢 Issue Count by Type:"
docker run --rm -v $(pwd):/app sentiment-backend flake8 sentiment_analysis/ | cut -d: -f4 | cut -d' ' -f2 | sort | uniq -c | sort -nr
echo

echo "📁 Issues by File:"
docker run --rm -v $(pwd):/app sentiment-backend flake8 sentiment_analysis/ | cut -d: -f1 | sort | uniq -c | sort -nr
echo

echo "🎯 Total Issues:"
docker run --rm -v $(pwd):/app sentiment-backend flake8 sentiment_analysis/ | wc -l
echo

echo "🔧 Most Problematic Lines (line length >200 chars):"
docker run --rm -v $(pwd):/app sentiment-backend flake8 sentiment_analysis/ | grep "E501" | awk -F">" '{print $2}' | awk '{print $1}' | sort -nr | head -5
echo

echo "⚡ Complex Functions:"
docker run --rm -v $(pwd):/app sentiment-backend flake8 sentiment_analysis/ | grep "C901" 