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
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_chat_completion(model_id, messages, temperature=0.7, max_tokens=4000):
    """Send a chat completion request to the Sourcegraph API."""
    
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
    
    try:
        print(f"🤖 Sending message to {model_id}...")
        print(f"⚙️  Temperature: {temperature}, Max Tokens: {max_tokens}")
        print(f"💬 Conversation has {len(messages)} messages")
        print("-" * 50)
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
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
            
            return assistant_message
        else:
            print("❌ No response received from the model")
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
            
            # Send the entire conversation to the API
            assistant_response = send_chat_completion(model_id, conversation_history, temperature, max_tokens)
            
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
