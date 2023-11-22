# Use an official Python runtime as a parent image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

WORKDIR /app/src

# Define the command to run your application
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
