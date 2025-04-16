FROM python:3.8-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn dj-database-url psycopg2-binary

# Copy project files
COPY . .

# Make start.sh executable
COPY start.sh .
RUN chmod +x start.sh

# Use the startup script
CMD ["./start.sh"]