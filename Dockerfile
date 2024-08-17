# Use the official Python image from the Docker Hub
FROM python:3.10.14-slim-bullseye

# Set environment variables to avoid writing .pyc files and enable unbuffered stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    gcc \
    g++ \
    git \
    libjpeg-dev \
    libpng-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Update pip and install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Install a compatible version of NumPy
RUN pip install "numpy<2"

# Install a specific version of OpenCV known to work well with NumPy 1.x
RUN pip install opencv-python-headless==4.5.5.64

# Copy the rest of the application files
COPY . .

# Make port 8000 available to the world outside this container
# EXPOSE 4900

# Run a specific command or script
CMD ["python", "main.py"]

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
