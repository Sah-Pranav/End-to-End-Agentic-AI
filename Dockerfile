# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variable for backend URL (used in container)
ENV BASE_URL=http://localhost:8001

# Expose port 8000 (Azure Web Apps use this for Streamlit)
EXPOSE 8000

# Create startup script that runs both services
# FastAPI on port 8001 (internal), Streamlit on port 8000 (external)
RUN echo '#!/bin/bash\n\
uvicorn main:app --host 0.0.0.0 --port 8001 &\n\
streamlit run app.py --server.port 8000 --server.address 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]

