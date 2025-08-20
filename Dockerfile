FROM python:3.9-slim

WORKDIR /app

# Install requests
RUN pip install --no-cache-dir requests argparse

# Copy the trigger script
COPY trigger_vectorization.py /app/trigger_vectorization.py

# Default command: run the script with no arguments (would error if missing --vectorizationUrl)
CMD ["python", "trigger_vectorization.py"]
