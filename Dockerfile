# Use the official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files into the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run the app
CMD ["python", "app.py"]
