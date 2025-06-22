#!/usr/bin/env python3
"""
Sourcegraph Cody API - List Available Models

This script demonstrates how to list all available LLM models from the Sourcegraph API.
It shows the model ID, creation date, and owner for each available model.

Usage:
    python 00-models.py

Make sure to set your environment variables in .env:
    SOURCEGRAPH_URL=https://sourcegraph.com
    SOURCEGRAPH_ACCESS_TOKEN=your_token_here
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_available_models():
    """Fetch and display all available models from the Sourcegraph API."""
    
    # Get configuration from environment
    base_url = os.getenv('SOURCEGRAPH_URL')
    access_token = os.getenv('SOURCEGRAPH_ACCESS_TOKEN')
    x_requested_with = os.getenv('SOURCEGRAPH_X_REQUESTED_WITH', 'cody-cookbook')
    
    if not base_url or not access_token:
        print("❌ Error: Please set SOURCEGRAPH_URL and SOURCEGRAPH_ACCESS_TOKEN in your .env file")
        return
    
    # API endpoint
    url = f"{base_url}/.api/llm/models"
    
    # Headers
    headers = {
        'Accept': 'application/json',
        'Authorization': f'token {access_token}',
        'X-Requested-With': x_requested_with
    }
    
    try:
        print(f"🔍 Fetching models from {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        models = data.get('data', [])
        
        print(f"\n✅ Found {len(models)} available models:\n")
        print(f"{'Model ID':<50} {'Owner':<15} {'Created'}")
        print("-" * 80)
        
        for model in models:
            model_id = model.get('id', 'N/A')
            owner = model.get('owned_by', 'N/A')
            created = model.get('created', 0)
            
            print(f"{model_id:<50} {owner:<15} {created}")
        
        print(f"\n💡 Tip: Copy a model ID to use in the next example (01-modelinstance.py)")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {response.status_code}: {e}")
        try:
            error_body = response.text
            print(f"📄 Response body: {error_body}")
        except:
            print("❌ Could not read response body")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making request: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON response: {e}")
        try:
            print(f"📄 Raw response: {response.text}")
        except:
            print("❌ Could not read response text")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    get_available_models()
