# Use the official Python base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install the vcan kernel module
RUN apt-get update && \
    apt-get install -y linux-modules-extra-$(uname -r)

# Copy the Python requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code files into the container
COPY rec.py .
COPY main.py .
COPY received_can_messages.csv .

# Run modprobe to load the vcan module
CMD modprobe vcan && \
    python -u rec.py && \
    python -u main.py
