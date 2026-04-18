# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for MySQL and standard build tools
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Exclude unnecessary files (alternatively handled by .dockerignore)
RUN rm -rf exports/* uploads/* reports_history.db scratch/ .env

# Create necessary directories
RUN mkdir -p exports uploads templates_word

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run uvicorn when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
