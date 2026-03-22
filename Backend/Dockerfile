# Use an official Python runtime as a parent image
# python:3.10-slim is a good balance of size and compatibility
FROM python:3.10-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# (Optional) If your 'LiveAgent' handles audio processing (like ffmpeg or portaudio),
# you might need to uncomment the following lines:
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     libportaudio2 \
#     && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# This copies main.py, nimipersonal/, and databaseop/ into /app
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
# We assume your python file is named "main.py". 
# If it is named "app.py", change "main:app" to "app:app"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]