#!/usr/bin/env python3
"""
Sourcegraph Cody API - Get Model Instance Details

This script demonstrates how to get detailed information about a specific model
using its model ID from the Sourcegraph API.

Usage:
    python 01-modelinstance.py <model_id>
    
Example:
    python 01-modelinstance.py anthropic::2024-10-22::claude-sonnet-4-latest

Make sure to set your environment variables in .env:
    SOURCEGRAPH_URL=https://sourcegraph.com
    SOURCEGRAPH_ACCESS_TOKEN=your_token_here
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_model_details(model_id):
    """Fetch and display details for a specific model."""
    
    # Get configuration from environment
    base_url = os.getenv('SOURCEGRAPH_URL')
    access_token = os.getenv('SOURCEGRAPH_ACCESS_TOKEN')
    x_requested_with = os.getenv('SOURCEGRAPH_X_REQUESTED_WITH', 'cody-cookbook')
    
    if not base_url or not access_token:
        print("❌ Error: Please set SOURCEGRAPH_URL and SOURCEGRAPH_ACCESS_TOKEN in your .env file")
        return
    
    # API endpoint
    url = f"{base_url}/.api/llm/models/{model_id}"
    
    # Headers
    headers = {
        'Accept': 'application/json',
        'Authorization': f'token {access_token}',
        'X-Requested-With': x_requested_with
    }
    
    try:
        print(f"🔍 Fetching details for model: {model_id}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        model = response.json()
        
        print(f"\n✅ Model Details:")
        print("-" * 50)
        print(f"ID:         {model.get('id', 'N/A')}")
        print(f"Object:     {model.get('object', 'N/A')}")
        print(f"Owner:      {model.get('owned_by', 'N/A')}")
        print(f"Created:    {model.get('created', 'N/A')}")
        
        print(f"\n💡 This model can be used for chat completions in the next example (02-chat.py)")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {response.status_code}: {e}")
        try:
            error_body = response.text
            print(f"📄 Response body: {error_body}")
            if response.status_code == 404:
                print(f"💡 Model '{model_id}' not found. Run 00-models.py to see available models")
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

def main():
    if len(sys.argv) != 2:
        print("Usage: python 01-modelinstance.py <model_id>")
        print("\nExample:")
        print("python 01-modelinstance.py anthropic::2024-10-22::claude-sonnet-4-latest")
        print("\n💡 Run 00-models.py first to see available model IDs")
        sys.exit(1)
    
    model_id = sys.argv[1]
    get_model_details(model_id)

if __name__ == "__main__":
    main()
