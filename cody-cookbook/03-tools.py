#!/usr/bin/env python3
"""
Sourcegraph Cody API - Function/Tool Calling with Full API Visibility

This script demonstrates tool calling with complete visibility into API payloads.
You'll see exactly what data is sent to and received from the Sourcegraph API.

Usage:
    python 03-tools.py [model_id]
    
Example:
    python 03-tools.py anthropic::2024-10-22::claude-sonnet-4-latest

Make sure to set your environment variables in .env:
    SOURCEGRAPH_URL=https://sourcegraph.com
    SOURCEGRAPH_ACCESS_TOKEN=your_token_here
    SOURCEGRAPH_X_REQUESTED_WITH=cody-cookbook
"""

import os
import sys
import json
import math
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils.file_utils import save_tool_calling_session_to_markdown

# Load environment variables from .env file
load_dotenv()

def get_current_weather(location, unit="celsius"):
    """Simulated weather function - in a real implementation, this would call a weather API."""
    weather_data = {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "description": "Partly cloudy",
        "humidity": 65,
        "wind_speed": 10
    }
    return json.dumps(weather_data)

def calculate_math(expression):
    """Safely evaluate mathematical expressions."""
    try:
        # Only allow safe mathematical operations
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }
        allowed_names.update({"__builtins__": {}})
        
        result = eval(expression, allowed_names)
        return json.dumps({"expression": expression, "result": result})
    except Exception as e:
        return json.dumps({"expression": expression, "error": str(e)})

def get_current_time():
    """Get the current date and time."""
    now = datetime.now()
    return json.dumps({
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "UTC",
        "day_of_week": now.strftime("%A")
    })

# Available functions that the AI can call
AVAILABLE_FUNCTIONS = {
    "get_current_weather": get_current_weather,
    "calculate_math": calculate_math,
    "get_current_time": get_current_time
}

def print_json_payload(title, payload, direction=""):
    """Pretty print JSON payloads with clear formatting."""
    print(f"\n{'='*80}")
    print(f"{direction} {title}")
    print(f"{'='*80}")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"{'='*80}")

def get_tools_definition():
    """Get the tools definition to send to the API."""
    return [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and country, e.g., 'San Francisco, CA'"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The temperature unit to use. Defaults to celsius."
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_math",
                "description": "Calculate mathematical expressions safely",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "A mathematical expression to evaluate, e.g., '2 + 2' or 'sin(pi/2)'"
                        }
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current date and time",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    ]

def execute_function_call(function_name, function_args):
    """Execute a function call and return the result."""
    print(f"\n🔧 EXECUTING LOCAL FUNCTION")
    print(f"   Function: {function_name}")
    print(f"   Arguments: {json.dumps(function_args, indent=2)}")
    
    if function_name in AVAILABLE_FUNCTIONS:
        try:
            if function_name == "get_current_weather":
                result = AVAILABLE_FUNCTIONS[function_name](
                    function_args.get('location'),
                    function_args.get('unit', 'celsius')
                )
            elif function_name == "calculate_math":
                result = AVAILABLE_FUNCTIONS[function_name](
                    function_args.get('expression')
                )
            elif function_name == "get_current_time":
                result = AVAILABLE_FUNCTIONS[function_name]()
            
            print(f"   ✅ Function executed successfully")
            print(f"   📤 Function result: {result}")
            return result
            
        except Exception as e:
            error_result = json.dumps({"error": str(e)})
            print(f"   ❌ Function execution failed: {str(e)}")
            print(f"   📤 Error result: {error_result}")
            return error_result
    else:
        error_result = json.dumps({"error": f"Unknown function: {function_name}"})
        print(f"   ❌ Unknown function: {function_name}")
        print(f"   📤 Error result: {error_result}")
        return error_result

def send_chat_request(messages, model_id, temperature=0.7, max_tokens=4000, capture_details=False):
    """Send a chat request to the Sourcegraph API and return the response with optional detailed capture."""
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
    
    # Get tools definition
    tools = get_tools_definition()
    
    # Create the payload
    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "tools": tools
    }
    
    # Initialize API details capture
    api_details = {} if capture_details else None
    
    # Show the outgoing payload
    print_json_payload("API REQUEST PAYLOAD", payload, "📤 SENDING TO API:")
    
    try:
        # Capture request details if needed
        if capture_details:
            api_details['url'] = url
            api_details['headers'] = {k: v for k, v in headers.items()}  # Copy headers
            api_details['request_payload'] = payload.copy()  # Copy payload
        
        print(f"\n🌐 Making API request to: {url}")
        
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
        
        # Show the incoming response
        print_json_payload("API RESPONSE PAYLOAD", data, "📥 RECEIVED FROM API:")
        
        # Return both data and API details if capturing
        if capture_details:
            return data, api_details
        return data
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {response.status_code}: {e}")
        try:
            error_body = response.text
            print(f"📄 Response body: {error_body}")
        except:
            print("❌ Could not read response body")
        if capture_details:
            return None, api_details
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making request: {e}")
        if capture_details:
            return None, api_details
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON response: {e}")
        try:
            print(f"📄 Raw response: {response.text}")
        except:
            print("❌ Could not read response text")
        if capture_details:
            return None, api_details
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if capture_details:
            return None, api_details
        return None

def handle_tool_calling_conversation(user_message, model_id, capture_session=False, temperature=0.7, max_tokens=4000):
    """Handle a complete tool calling conversation with full API visibility and optional session capture."""
    print(f"\n🚀 Starting tool calling conversation")
    print(f"📝 User message: {user_message}")
    print(f"🤖 Model: {model_id}")
    
    # Session tracking variables
    session_start_time = time.time()
    session_steps = []
    total_api_calls = 0
    total_tool_calls = 0
    
    # Initialize conversation with user message
    conversation = [
        {
            "role": "user",
            "content": user_message
        }
    ]
    
    # Step 1: Send initial request to AI
    print(f"\n🔄 STEP 1: Sending initial request to AI")
    
    # Send request with details capture if needed
    if capture_session:
        result = send_chat_request(conversation, model_id, temperature, max_tokens, capture_details=True)
        if isinstance(result, tuple):
            response, api_details = result
        else:
            response = result
            api_details = None
    else:
        response = send_chat_request(conversation, model_id, temperature, max_tokens)
        api_details = None
    
    total_api_calls += 1
    
    if not response or 'choices' not in response or len(response['choices']) == 0:
        print("❌ No valid response received from API")
        return None if not capture_session else None
    
    message_response = response['choices'][0]['message']
    
    # Capture initial request step
    if capture_session and api_details:
        session_steps.append({
            'step_number': 1,
            'step_type': 'initial_request',
            'user_query': user_message,
            'api_details': api_details
        })
    
    # Add assistant's response to conversation
    conversation.append(message_response)
    
    # Check if AI wants to call tools
    if 'tool_calls' in message_response and message_response['tool_calls']:
        print(f"\n🔄 STEP 2: AI decided to call {len(message_response['tool_calls'])} tool(s)")
        
        # Capture tool execution details
        tool_calls_details = []
        
        # Process each tool call
        for i, tool_call in enumerate(message_response['tool_calls'], 1):
            function_name = tool_call['function']['name']
            function_args = json.loads(tool_call['function']['arguments'])
            tool_call_id = tool_call.get('id', f'call_{i}')
            
            print(f"\n   🔧 Tool Call #{i}:")
            print(f"      Function: {function_name}")
            print(f"      Arguments: {json.dumps(function_args, indent=2)}")
            print(f"      Call ID: {tool_call_id}")
            
            # Execute the function locally
            function_result = execute_function_call(function_name, function_args)
            
            total_tool_calls += 1
            
            # Capture tool call details
            if capture_session:
                tool_calls_details.append({
                    'function_name': function_name,
                    'function_args': function_args,
                    'call_id': tool_call_id,
                    'function_result': function_result
                })
            
            # Add tool result to conversation
            tool_message = {
                "tool_call_id": tool_call_id,
                "role": "assistant",
                "name": function_name,
                "content": function_result
            }
            conversation.append(tool_message)
        
        # Capture tool execution step
        if capture_session:
            session_steps.append({
                'step_number': 2,
                'step_type': 'tool_execution',
                'tool_calls': tool_calls_details
            })
        
        # Step 3: Send conversation with tool results back to AI
        print(f"\n🔄 STEP 3: Sending tool results back to AI for final response")
        
        # Send final request with details capture if needed
        if capture_session:
            result = send_chat_request(conversation, model_id, temperature, max_tokens, capture_details=True)
            if isinstance(result, tuple):
                final_response, final_api_details = result
            else:
                final_response = result
                final_api_details = None
        else:
            final_response = send_chat_request(conversation, model_id, temperature, max_tokens)
            final_api_details = None
        
        total_api_calls += 1
        
        if final_response and 'choices' in final_response and len(final_response['choices']) > 0:
            final_message = final_response['choices'][0]['message']
            final_content = final_message.get('content', '')
            
            if final_content:
                print(f"\n🎯 FINAL AI RESPONSE:")
                print(f"🤖 Assistant: {final_content}")
                
                # Capture final response step
                if capture_session and final_api_details:
                    session_steps.append({
                        'step_number': 3,
                        'step_type': 'final_response',
                        'ai_response': final_content,
                        'api_details': final_api_details
                    })
            else:
                print(f"\n🎯 AI provided tool results but no additional text response")
        else:
            print(f"\n❌ No final response received from AI")
            
    else:
        # No tool calls - direct response
        print(f"\n🔄 AI provided direct response (no tools needed)")
        if message_response.get('content'):
            print(f"\n🎯 AI RESPONSE:")
            print(f"🤖 Assistant: {message_response['content']}")
            
            # Capture direct response step
            if capture_session and api_details:
                session_steps.append({
                    'step_number': 2,
                    'step_type': 'final_response',
                    'ai_response': message_response.get('content'),
                    'api_details': api_details
                })
        else:
            print(f"\n❌ No content in AI response")
    
    # Show usage stats if available
    if 'usage' in response:
        usage = response['usage']
        print(f"\n📊 API Usage Statistics:")
        print(f"   Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
        print(f"   Completion tokens: {usage.get('completion_tokens', 'N/A')}")
        print(f"   Total tokens: {usage.get('total_tokens', 'N/A')}")
    
    # Return session data if capturing
    if capture_session:
        session_duration = time.time() - session_start_time
        session_duration_str = f"{int(session_duration // 60)}m {int(session_duration % 60)}s"
        
        # Prepare available tools info
        available_tools = []
        for tool_def in get_tools_definition():
            if 'function' in tool_def:
                func = tool_def['function']
                available_tools.append({
                    'name': func.get('name', 'Unknown'),
                    'description': func.get('description', 'No description')
                })
        
        session_metadata = {
            'model_id': model_id,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'duration': session_duration_str,
            'total_api_calls': total_api_calls,
            'total_tool_calls': total_tool_calls,
            'user_query': user_message,
            'available_tools': available_tools,
            'complete_conversation': conversation
        }
        
        return {
            'session_steps': session_steps,
            'session_metadata': session_metadata
        }
    
    return None

def interactive_mode(model_id):
    """Interactive mode for testing tool calling with session capture."""
    print(f"\n💬 Interactive Tool Calling Mode")
    print(f"🤖 Model: {model_id}")
    print(f"🛠️  Available tools: weather, math calculator, current time")
    print(f"📋 Commands: 'quit'/'exit' to end, 'clear' to clear screen, 'temp'/'tokens' to adjust settings")
    print("-" * 70)
    
    # Settings
    temperature = 0.7
    max_tokens = 4000
    session_count = 0
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'clear':
                os.system('clear' if os.name == 'posix' else 'cls')
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
            
            # Handle the tool calling conversation with session capture
            session_data = handle_tool_calling_conversation(
                user_input, 
                model_id, 
                capture_session=True,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Save session if data was captured
            if session_data:
                session_count += 1
                script_name = os.path.splitext(os.path.basename(__file__))[0]
                saved_path = save_tool_calling_session_to_markdown(
                    session_data['session_steps'],
                    session_data['session_metadata'],
                    script_name
                )
                
                if saved_path:
                    print(f"\n📁 Session #{session_count} saved to: {saved_path}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

def run_examples(model_id):
    """Run predefined examples to demonstrate tool calling with session capture."""
    examples = [
        "What time is it?",
        "Calculate the square root of 144",
        "What's the weather like in San Francisco?",
        "What's 15 * 23?",
        "Can you tell me the weather in Tokyo and also calculate sin(pi/2)?",
    ]
    
    print(f"\n🧪 Running {len(examples)} tool calling examples:")
    print("💡 You'll see the complete API communication for each example")
    print("📁 Each example will be saved as a detailed session file")
    print("-" * 70)
    
    for i, example in enumerate(examples, 1):
        print(f"\n📝 EXAMPLE {i}/{len(examples)}: {example}")
        
        # Handle the tool calling conversation with session capture
        session_data = handle_tool_calling_conversation(
            example, 
            model_id, 
            capture_session=True
        )
        
        # Save session if data was captured
        if session_data:
            script_name = os.path.splitext(os.path.basename(__file__))[0]
            saved_path = save_tool_calling_session_to_markdown(
                session_data['session_steps'],
                session_data['session_metadata'],
                script_name
            )
            
            if saved_path:
                print(f"\n📁 Example #{i} session saved to: {saved_path}")
        
        if i < len(examples):
            input(f"\n⏸️  Press Enter to continue to example {i+1}...")

def main():
    # Default model
    default_model = "anthropic::2024-10-22::claude-sonnet-4-latest"
    
    if len(sys.argv) > 1:
        model_id = sys.argv[1]
    else:
        model_id = default_model
        print(f"💡 Using default model: {model_id}")
    
    print("\n🛠️  SOURCEGRAPH CODY API - TOOL CALLING WITH FULL API VISIBILITY")
    print("=" * 70)
    print("This script shows you EXACTLY what happens during tool calling:")
    print("   📤 Complete API request payloads sent to Sourcegraph")
    print("   📥 Complete API response payloads received from AI") 
    print("   🔧 Local function executions and results")
    print("   🔄 Multi-step conversation flow with tool results")
    print("=" * 70)
    print("\n🎯 Available Tools:")
    print("   🌤️  get_current_weather(location, unit) - Get weather for a location")
    print("   🧮 calculate_math(expression) - Safely evaluate math expressions")
    print("   ⏰ get_current_time() - Get current date and time")
    
    choice = input("\nChoose mode:\n1. 📚 Run examples with full API visibility\n2. 💬 Interactive mode\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        run_examples(model_id)
        print(f"\n🎉 Examples complete! Want to try interactive mode?")
        if input("Start interactive mode? (y/n): ").lower() in ['y', 'yes']:
            interactive_mode(model_id)
    elif choice == "2":
        interactive_mode(model_id)
    else:
        print("Invalid choice. Starting with examples...")
        run_examples(model_id)

if __name__ == "__main__":
    main()
