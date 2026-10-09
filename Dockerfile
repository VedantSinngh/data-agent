# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project configuration and source
COPY pyproject.toml .
COPY README.md .
COPY app/ ./app/
COPY data/ ./data/

# Install the dependencies
RUN pip install --no-cache-dir hatchling
RUN pip install --no-cache-dir .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
