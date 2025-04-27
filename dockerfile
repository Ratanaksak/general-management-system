FROM python:3.9-slim

# Install system dependencies required for building packages like scipy
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up a virtual environment and install dependencies
RUN python -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip
COPY requirements.txt .
RUN /opt/venv/bin/pip install -r requirements.txt

# Set the working directory to /app
WORKDIR /app
COPY . /app/

# Expose the port that the app will run on (usually 8000 for Django)
EXPOSE 8000

# Start the app
CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000"]
