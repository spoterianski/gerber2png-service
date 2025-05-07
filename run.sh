#!/bin/bash

# Запуск тестов с покрытием
docker compose run --rm backend pytest tests/ -v --cov=. --cov-report=term-missing

TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "Tests passed successfully! Building the application..."
    docker compose build
    docker compose up
else
    echo "Tests failed! Please fix the issues before building."
    exit $TEST_EXIT_CODE
fi 