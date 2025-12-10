# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose your app port (change if needed)
EXPOSE 8000

# Start your Python app
CMD ["python", "app.py"]
