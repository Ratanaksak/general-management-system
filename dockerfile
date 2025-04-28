FROM python:3.11-slim  # Use a supported Python version (3.11 or 3.12)

# Install build dependencies (including gfortran)
RUN apt-get update && \
    apt-get install -y gfortran build-essential && \
    rm -rf /var/lib/apt/lists/*
# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "manage.py"]  # Replace with your startup command