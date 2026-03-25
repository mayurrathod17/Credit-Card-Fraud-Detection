FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (required for some ML packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port (8000 is default for FastAPI)
EXPOSE 8000

# Command to run the FastApi application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
