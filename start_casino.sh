#!/bin/bash

# Navigate to the project root directory
cd "$(dirname "$0")"

# Install Python dependencies using Poetry
echo "Installing Python dependencies..."
poetry install

# Start the Python backend
echo "Starting Python backend..."
poetry run python gomboc_gambling/gambling.py &
BACKEND_PID=$!

# Navigate to the frontend directory and start the React frontend
echo "Starting React frontend..."
cd frontend
npm install
npm start &
FRONTEND_PID=$!

# Function to clean up and stop the processes
cleanup() {
    echo "Stopping frontend and backend..."
    kill $FRONTEND_PID
    kill $BACKEND_PID
    wait $FRONTEND_PID
    wait $BACKEND_PID
    echo "Stopped all services."
}

# Trap SIGINT and SIGTERM to clean up properly
trap cleanup SIGINT SIGTERM

# Wait for frontend and backend to finish
wait $FRONTEND_PID
wait $BACKEND_PID

