# Use a slim, official Python 3.11 base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy ONLY the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Python doesn't buffer logs (critical for viewing real-time logs in AWS/Cloud)
ENV PYTHONUNBUFFERED=1

# Copy the rest of your application code
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Run Streamlit in Headless mode so it doesn't freeze asking for an email!
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]