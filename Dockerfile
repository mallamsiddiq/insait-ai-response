FROM python:3.11-alpine

# Set environment variables to optimize Python behavior in the container
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app/

# update pip
RUN pip install --upgrade pip

# Install the project dependencies using Poetry
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

RUN alembic upgrade head

# Expose the port the app will run on
EXPOSE 5000


# Command to run the application (assuming run.py is your entry point)
CMD ["python", "run.py"]