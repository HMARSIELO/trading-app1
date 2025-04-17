# Use official Python 3.10 base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .

# Optional: install build tools if needed for numpy/pandas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --default-timeout=3000 -r requirements.txt

# Copy the rest of the application
COPY . .

# Start the app

CMD ["gunicorn", "main:app", "-c", "gunicorn_config.py"]

