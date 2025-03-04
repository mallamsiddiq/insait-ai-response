FROM python:3.11-alpine

# Set environment variables to optimize Python behavior in the container
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install pg_isready and bash
RUN apk add --no-cache bash postgresql-client

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 5000

# Wait for the PostgreSQL database to be ready
CMD ["sh", "-c", "until pg_isready -h db -p 5432; do echo 'Waiting for database...'; sleep 2; done; alembic upgrade head; python run.py"]
