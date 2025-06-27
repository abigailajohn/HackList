# Use official Python image
FROM python:3.22-alpine

# Set working directory
WORKDIR /app

# Install system dependencies (if any needed for pip packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Set environment variables for Streamlit (optional, can be overridden)
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false

# Entrypoint to run the Streamlit app
CMD ["streamlit", "run", "app.py"] 