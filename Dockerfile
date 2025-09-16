FROM python:3.12-slim
LABEL authors="futc"

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /web-flask

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Expose port for Flask
EXPOSE 8000

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /web-flask
USER appuser

# Command to run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "1", "--threads", "4", "app:app"]