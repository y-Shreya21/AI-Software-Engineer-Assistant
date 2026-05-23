# Use a lightweight official Python 3.11 image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (git is required by GitPython to clone repos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the FastAPI application on port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
