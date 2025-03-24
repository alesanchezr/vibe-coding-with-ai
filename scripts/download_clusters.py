#!/usr/bin/env python3

import os
import json
import requests
from dotenv import load_dotenv

def download_clusters():
    # Load environment variables from .env file
    load_dotenv(override=True)
    
    # Get required environment variables
    bc_api_url = os.getenv("BC_API_URL")
    bc_token = os.getenv("BC_TOKEN")
    bc_academies = os.getenv("BC_ACADEMIES")
    
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
    
    # Initialize list to store all clusters
    all_clusters = []
    
    # Make requests for each academy
    for academy_id in academy_ids:
        print(f"Downloading clusters for academy ID: {academy_id}")
        
        # Set academy ID in header
        request_headers = {**headers, "Academy": academy_id}
        
        # Make API request
        try:
            response = requests.get(
                f"{bc_api_url}/registry/academy/keywordcluster",
                headers=request_headers
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse response
            clusters = response.json()
            
            # Add academy ID to each cluster for reference
            for cluster in clusters:
                cluster["academy_id"] = academy_id
            
            # Add to all clusters
            all_clusters.extend(clusters)
            
            print(f"Successfully downloaded {len(clusters)} clusters for academy ID: {academy_id}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading clusters for academy ID {academy_id}: {e}")
    
    # Save all clusters to file
    if all_clusters:
        try:
            with open("scripts/clusters.json", "w") as f:
                json.dump(all_clusters, f, indent=2)
            print(f"Successfully saved {len(all_clusters)} clusters to scripts/clusters.json")
        except Exception as e:
            print(f"Error saving clusters to file: {e}")
    else:
        print("No clusters were downloaded. Check your API credentials and academy IDs.")

if __name__ == "__main__":
    download_clusters() 