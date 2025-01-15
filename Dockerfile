# Use the Official Python Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy Requirements
COPY requirements.txt /app

# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose port 5000
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Run the application
CMD ["python","app.py"]

