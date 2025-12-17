# Use an official Python runtime as a parent image
FROM python:3.9-slim

# --- Install GeoDjango System Dependencies ---
# These are required for PostGIS functionality (GDAL, GEOS, PROJ)
# Using apk for Alpine-based python:3.9-slim image
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
