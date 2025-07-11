# Start from Python 3.12 slim image
FROM python:3.12-slim

# Install build dependencies including gfortran and ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gfortran \
    build-essential \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory in container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files into the container
COPY . .

# Set the environment variable to make Django run in production mode (optional)
# ENV DJANGO_SETTINGS_MODULE=myproject.settings.production

# Expose the port the app runs on (default Django port 8000)
EXPOSE 8000

# Command to start the Django app (can be replaced with gunicorn for production)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "core.wsgi:application"]
