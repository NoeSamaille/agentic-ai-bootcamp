# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker caching
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code into the container
COPY app.py /app/

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run uvicorn server on container start
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
