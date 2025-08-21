#!/usr/bin/env python
import requests
import logging
import sys
import argparse
import os
import json
from pathlib import Path

def main():
    # Setup centralized logging
    try:
        from logging_config import setup_service_logging
        logger_instance = setup_service_logging('trigger-vectorization-pipeline')
        logger_instance.log_action("Starting Vectorization Pipeline Trigger")
        centralized_logging = True
    except ImportError:
        # Fallback for environments without centralized logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
        logging.info("Starting Vectorization Pipeline Trigger - fallback logging")
        centralized_logging = False

    parser = argparse.ArgumentParser(description="Trigger the Vectorization Service via a POST request.")
    parser.add_argument("--vectorizationServiceUrl", required=True,
                        help="Base URL of the Vectorization Service (e.g. http://localhost:5001)")
    parser.add_argument("--url", required=True,
                        help="The dataset URL to be vectorized.")
    parser.add_argument("--jobId", required=True,
                        help="Unique Job ID for the vectorization/aggregation process.")
    parser.add_argument("--clientsList", required=True,
                        help="List of client identifiers as JSON array (e.g., --clientsList '[\"client1\", \"client2\"]')")
    parser.add_argument("--studyId", required=True,
                        help="Study identifier for Feature Extraction Tool API (required for both dev and prod modes)")
    # orchestratorUrl is now configured via environment variable in vectorization service
    args = parser.parse_args()

    # Parse clientsList - Robust parsing for shell compatibility
    try:
        # First try standard JSON parsing
        try:
            clients_list = json.loads(args.clientsList)
        except json.JSONDecodeError:
            # If standard JSON fails, try to fix common shell quote issues
            fixed_input = args.clientsList.strip()
            
            # Handle shell-stripped quotes: [client1, client2] -> ["client1", "client2"]
            if fixed_input.startswith('[') and fixed_input.endswith(']'):
                # Extract content between brackets
                content = fixed_input[1:-1].strip()
                if content:
                    # Split by comma and clean each item
                    items = [item.strip().strip('"\'') for item in content.split(',')]
                    clients_list = [item for item in items if item]
                else:
                    clients_list = []
            else:
                # Try to parse as single value and wrap in list
                cleaned = args.clientsList.strip().strip('"\'')
                clients_list = [cleaned] if cleaned else []
        
        # Validate that it's a list of strings
        if not isinstance(clients_list, list):
            raise ValueError("clientsList must resolve to a list")
        if not clients_list:
            raise ValueError("clientsList cannot be empty")
        if not all(isinstance(client, str) and client.strip() for client in clients_list):
            raise ValueError("All clients must be non-empty strings")
            
        logging.info(f"Parsed clientsList: {clients_list}")
        
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"Invalid clientsList format: {args.clientsList}")
        logging.error(f"Supported formats:")
        logging.error(f"  - JSON array: '[\"client1\", \"client2\"]'")
        logging.error(f"  - Simple array: '[client1, client2]'")
        logging.error(f"  - Single value: 'client1'")
        logging.error(f"Error: {e}")
        sys.exit(1)

    # Construct the POST body from the arguments
    request_body = {
        "url": args.url,
        "jobId": args.jobId,
        "clientsList": clients_list,  # Normalized to proper Python list
        "studyId": args.studyId  # Always required now
    }

    # Build the full endpoint for the Vectorization Service
    vectorize_endpoint = f"{args.vectorizationServiceUrl.rstrip('/')}/vectorize"

    logging.info(f"Sending POST to {vectorize_endpoint} with body: {request_body}")

    # POST request to the Vectorization Service
    try:
        logging.info("Initiating HTTP POST request to vectorization service")
        resp = requests.post(vectorize_endpoint, json=request_body, timeout=30)
        logging.info(f"Response code: {resp.status_code}")
        logging.info(f"Response body: {resp.text}")
    except Exception as e:
        logging.error(f"Error sending request: {e}")
        sys.exit(1)

    # Treat non-200 as failure
    if resp.status_code != 200:
        logging.error("Vectorization trigger request failed.")
        sys.exit(1)

    logging.info("Vectorization trigger request succeeded.")

if __name__ == "__main__":
    main()