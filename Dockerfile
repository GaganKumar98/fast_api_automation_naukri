# Use a Python base image
FROM python:3.10-slim

# Set a working directory
WORKDIR /app

# Copy the requirements.txt first, to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /app/

# Expose the port that your app will run on
EXPOSE 8000

# Set environment variable for uvicorn
ENV PORT=8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
