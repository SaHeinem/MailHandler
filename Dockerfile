FROM python:3.11-slim

# In a Docker DEV container, writing .pyc files is generally unnecessary because the container is often short-lived
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure that logs and output messages appear in real-time
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && apt-get clean

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 8000 for the Django server
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]