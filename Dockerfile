# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev cron \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port the app runs on
EXPOSE 8000

RUN echo "0 * * * * root python /app/manage.py update_nav >> /var/log/cron.log 2>&1" > /etc/cron.d/hourly-task
RUN chmod 0644 /etc/cron.d/hourly-task
RUN touch /var/log/cron.log


# Start cron in the background
CMD cron && tail -f /var/log/cron.log && python manage.py runserver 0.0.0.0:8000
