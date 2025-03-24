#!/usr/bin/env python3

import os
import json
import requests
from dotenv import load_dotenv

def download_technologies():
    # Reload environment variables from .env file to ensure we have the latest
    load_dotenv(override=True)
    
    # Get required environment variables
    bc_api_url = os.getenv("BC_API_URL")
    bc_token = os.getenv("BC_TOKEN")
    bc_academies = os.getenv("BC_ACADEMIES")
    
    # Print the token being used (first 10 chars only for security)
    print(f"Using token from .env: {bc_token[:10]}...")
    
    # Validate environment variables
    if not bc_api_url or not bc_token or not bc_academies:
        print("Error: Required environment variables not found.")
        print("Please ensure BC_API_URL, BC_TOKEN, and BC_ACADEMIES are defined in your .env file.")
        return
    
    # Parse academy IDs
    academy_ids = [id.strip() for id in bc_academies.split(",")]
    
    # Prepare headers for API request
    headers = {
        "Authorization": f"Token {bc_token}",
    }
    
    # Initialize list to store all technologies
    all_technologies = []
    
    # Make requests for each academy
    for academy_id in academy_ids:
        print(f"Downloading technologies for academy ID: {academy_id}")
        
        # Set academy ID in header
        request_headers = {**headers, "Academy": academy_id}
        
        # Make API request
        print(f"Request headers: {request_headers}")
        try:
            # The BC_API_URL already includes /v1
            response = requests.get(
                f"{bc_api_url}/registry/academy/technology",
                headers=request_headers
            )
            
            # Try to get response content regardless of status code
            try:
                response_content = response.json()
                print(f"Response status: {response.status_code} {bc_token}")
                print(f"Response content: {response_content}")
            except Exception as json_error:
                print(f"Could not parse response as JSON: {response.text}")
            
            # Now check if the request was successful
            response.raise_for_status()
            
            # Parse response
            technologies = response.json()
            
            # Add academy ID to each technology for reference
            for technology in technologies:
                technology["academy_id"] = academy_id
            
            # Add to all technologies
            all_technologies.extend(technologies)
            
            print(f"Successfully downloaded {len(technologies)} technologies for academy ID: {academy_id}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading technologies for academy ID {academy_id}: {e}")
    
    # Save all technologies to file
    if all_technologies:
        try:
            with open("scripts/technologies.json", "w") as f:
                json.dump(all_technologies, f, indent=2)
            print(f"Successfully saved {len(all_technologies)} technologies to scripts/technologies.json")
        except Exception as e:
            print(f"Error saving technologies to file: {e}")
    else:
        print("No technologies were downloaded. Check your API credentials and academy IDs.")

if __name__ == "__main__":
    download_technologies() 