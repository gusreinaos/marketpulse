# Author: Oscar Reina

# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.11.4-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
