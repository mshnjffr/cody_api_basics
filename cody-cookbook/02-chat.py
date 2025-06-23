#!/usr/bin/env python3
"""
Sourcegraph Cody API - Chat Completions

This script demonstrates how to send chat completion requests to the Sourcegraph API.
It allows users to specify temperature, max_tokens, and interactive chat with AI models.

Usage:
    python 02-chat.py [model_id]
    
Example:
    python 02-chat.py anthropic::2024-10-22::claude-sonnet-4-latest

If no model_id is provided, it defaults to Claude 4 Sonnet.

Make sure to set your environment variables in .env:
    SOURCEGRAPH_URL=https://sourcegraph.com
    SOURCEGRAPH_ACCESS_TOKEN=your_token_here
"""

import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
from utils.file_utils import save_chat_session_to_markdown

# Load environment variables from .env file
load_dotenv()

def send_chat_completion(model_id, messages, temperature=0.7, max_tokens=4000, capture_details=False):
    """Send a chat completion request to the Sourcegraph API with optional detailed capture."""
    
    # Get configuration from environment
    base_url = os.getenv('SOURCEGRAPH_URL')
    access_token = os.getenv('SOURCEGRAPH_ACCESS_TOKEN')
    x_requested_with = os.getenv('SOURCEGRAPH_X_REQUESTED_WITH', 'cody-cookbook')
    
    if not base_url or not access_token:
        print("❌ Error: Please set SOURCEGRAPH_URL and SOURCEGRAPH_ACCESS_TOKEN in your .env file")
        return None
    
    # API endpoint
    url = f"{base_url}/.api/llm/chat/completions"
    
    # Headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'token {access_token}',
        'X-Requested-With': x_requested_with
    }
    
    # Request payload
    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    # Initialize API details capture
    api_details = {} if capture_details else None
    
    try:
        print(f"🤖 Sending message to {model_id}...")
        print(f"⚙️  Temperature: {temperature}, Max Tokens: {max_tokens}")
        print(f"💬 Conversation has {len(messages)} messages")
        print("-" * 50)
        
        # Capture request details if needed
        if capture_details:
            api_details['url'] = url
            api_details['headers'] = {k: v for k, v in headers.items()}  # Copy headers
            api_details['request_payload'] = payload.copy()  # Copy payload
        
        # Record request time
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload)
        response_time = int((time.time() - start_time) * 1000)  # Convert to ms
        
        response.raise_for_status()
        
        data = response.json()
        
        # Capture response details if needed
        if capture_details:
            api_details['status_code'] = response.status_code
            api_details['response_time'] = response_time
            api_details['response_data'] = data.copy()
            api_details['usage'] = data.get('usage', {})
        
        # Extract the response
        if 'choices' in data and len(data['choices']) > 0:
            assistant_message = data['choices'][0]['message']['content']
            print(f"🤖 Assistant: {assistant_message}")
            
            # Show usage stats if available
            if 'usage' in data:
                usage = data['usage']
                print(f"\n📊 Usage Stats:")
                print(f"   Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
                print(f"   Completion tokens: {usage.get('completion_tokens', 'N/A')}")
                print(f"   Total tokens: {usage.get('total_tokens', 'N/A')}")
            
            # Return both message and API details
            if capture_details:
                return assistant_message, api_details
            return assistant_message
        else:
            print("❌ No response received from the model")
            if capture_details:
                return None, api_details
            return None
            
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {response.status_code}: {e}")
        try:
            error_body = response.text
            print(f"📄 Response body: {error_body}")
        except:
            print("❌ Could not read response body")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON response: {e}")
        try:
            print(f"📄 Raw response: {response.text}")
        except:
            print("❌ Could not read response text")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if capture_details:
            return None, api_details
        return None

def interactive_chat(model_id):
    """Run an interactive chat session with conversation memory."""
    print(f"🚀 Starting interactive chat with {model_id}")
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("You can also type 'temp' to change temperature, 'tokens' to change max tokens, or 'clear' to clear conversation history")
    print("-" * 70)
    
    temperature = 0.7
    max_tokens = 4000
    conversation_history = []  # Store the entire conversation
    session_start_time = time.time()
    api_calls_count = 0
    api_calls_history = []  # Store all API call details
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'clear':
                conversation_history = []
                print("✅ Conversation history cleared")
                continue
            elif user_input.lower() == 'temp':
                try:
                    new_temp = float(input("Enter new temperature (0.0-1.0): "))
                    if 0.0 <= new_temp <= 1.0:
                        temperature = new_temp
                        print(f"✅ Temperature set to {temperature}")
                    else:
                        print("❌ Temperature must be between 0.0 and 1.0")
                except ValueError:
                    print("❌ Invalid temperature value")
                continue
            elif user_input.lower() == 'tokens':
                try:
                    new_tokens = int(input("Enter max tokens (1-4000): "))
                    if 1 <= new_tokens <= 4000:
                        max_tokens = new_tokens
                        print(f"✅ Max tokens set to {max_tokens}")
                    else:
                        print("❌ Max tokens must be between 1 and 4000")
                except ValueError:
                    print("❌ Invalid token value")
                continue
            elif not user_input:
                print("Please enter a message")
                continue
            
            # Add user message to conversation history
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Send the entire conversation to the API with details capture
            result = send_chat_completion(model_id, conversation_history, temperature, max_tokens, capture_details=True)
            api_calls_count += 1
            
            # Handle response (could be tuple or single value)
            if isinstance(result, tuple):
                assistant_response, api_details = result
                api_calls_history.append(api_details)  # Store this API call
            else:
                assistant_response = result
            
            # Add assistant response to conversation history
            if assistant_response:
                conversation_history.append({
                    "role": "assistant",
                    "content": assistant_response
                })
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
    
    # Save session details when chat ends
    if conversation_history:
        session_duration = time.time() - session_start_time
        session_duration_str = f"{int(session_duration // 60)}m {int(session_duration % 60)}s"
        
        session_metadata = {
            'model_id': model_id,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'duration': session_duration_str,
            'api_calls_count': api_calls_count
        }
        
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        saved_path = save_chat_session_to_markdown(
            conversation_history, 
            api_calls_history, 
            session_metadata, 
            script_name
        )
        
        if saved_path:
            print(f"\n📁 Chat session saved to: {saved_path}")
    else:
        print("\n📝 No conversation to save.")

def main():
    # Default model
    default_model = "anthropic::2024-10-22::claude-sonnet-4-latest"
    
    if len(sys.argv) > 1:
        model_id = sys.argv[1]
    else:
        model_id = default_model
        print(f"💡 Using default model: {model_id}")
        print("💡 Run 00-models.py to see all available models")
    
    # Quick test message
    print(f"\n🧪 Testing with a quick message:")
    test_messages = [{"role": "user", "content": "Say hello and introduce yourself briefly!"}]
    send_chat_completion(model_id, test_messages, 0.7, 100)
    
    print(f"\n" + "="*70)
    
    # Start interactive chat
    interactive_chat(model_id)

if __name__ == "__main__":
    main()
