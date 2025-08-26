#!/bin/bash
# Run the FastAPI application using uvicorn
# The --host 0.0.0.0 makes the server accessible from outside localhost
# The --port 8000 is the default FastAPI port
uvicorn main:app --host 0.0.0.0 --port 8088 --reload
