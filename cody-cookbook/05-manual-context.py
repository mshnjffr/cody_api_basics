#!/usr/bin/env python3
"""
Sourcegraph Cody API - Manual Context Passing

This script demonstrates how to manually pass context to the Cody API for code analysis,
refactoring, and improvement suggestions. Instead of searching for context, we provide
specific code files or snippets directly to the AI.

All AI responses are automatically saved to timestamped files in the 'responses/' directory
for easy reading and future reference.

Usage:
    python 05-manual-context.py [model_id]
    
Example:
    python 05-manual-context.py anthropic::2024-10-22::claude-sonnet-4-latest

Make sure to set your environment variables in .env:
    SOURCEGRAPH_URL=https://sourcegraph.com
    SOURCEGRAPH_ACCESS_TOKEN=your_token_here
    SOURCEGRAPH_X_REQUESTED_WITH=cody-cookbook
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def read_context_file(file_path):
    """Read a file to use as context for the AI."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"✅ Successfully read context file: {file_path}")
        print(f"📄 File size: {len(content)} characters")
        return content
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"❌ Error reading file '{file_path}': {e}")
        return None

def save_response_to_file(content, task_name="response", context_description="unknown"):
    """Save AI response to a file with timestamp."""
    # Create responses directory if it doesn't exist
    responses_dir = "responses"
    if not os.path.exists(responses_dir):
        os.makedirs(responses_dir)
        print(f"📁 Created responses directory: {responses_dir}")
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_task_name = "".join(c for c in task_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_task_name = safe_task_name.replace(' ', '_').lower()
    filename = f"{timestamp}_{safe_task_name}.md"
    filepath = os.path.join(responses_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            # Write header with metadata
            file.write(f"# AI Response: {task_name}\n\n")
            file.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            file.write(f"**Context:** {context_description}\n\n")
            file.write("---\n\n")
            file.write(content)
        
        print(f"💾 Response saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving response to file: {e}")
        return None

def send_chat_with_context(model_id, user_message, context_content, context_description="Code context", temperature=0.7, max_tokens=4000, save_to_file=True, task_name=None):
    """Send a chat request with manual context to the Sourcegraph API."""
    
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
    
    # Create messages with context (Note: Sourcegraph API doesn't support "system" role)
    messages = [
        {
            "role": "user", 
            "content": f"You are a senior software engineer helping with code review and refactoring. You have been provided with {context_description} to analyze and improve.\n\nHere is the context you should analyze:\n\n```\n{context_content}\n```\n\n{user_message}"
        }
    ]
    
    # Request payload
    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    print(f"\n🤖 Sending request to {model_id}")
    print(f"📝 Context description: {context_description}")
    print(f"💬 User message: {user_message}")
    print(f"⚙️  Temperature: {temperature}, Max tokens: {max_tokens}")
    print(f"📦 Total context size: {len(context_content)} characters")
    print("-" * 70)
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        if 'choices' in data and len(data['choices']) > 0:
            assistant_message = data['choices'][0]['message']['content']
            print(f"🤖 AI Response:\n{assistant_message}")
            
            # Save response to file if requested
            if save_to_file:
                file_task_name = task_name or user_message[:50].replace('\n', ' ')
                saved_path = save_response_to_file(assistant_message, file_task_name, context_description)
                if saved_path:
                    print(f"📁 Full response available in: {saved_path}")
            
            # Show usage stats if available
            if 'usage' in data:
                usage = data['usage']
                print(f"\n📊 Usage Statistics:")
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

def run_refactoring_examples(model_id, context_file="sample-code.md"):
    """Run predefined refactoring examples using the context file."""
    
    # Read the context file
    print(f"📚 Reading context from file: {context_file}")
    context_content = read_context_file(context_file)
    if not context_content:
        return
    
    # Define refactoring tasks
    refactoring_tasks = [
        {
            "task": "Security Review",
            "prompt": "Please review this code for security vulnerabilities and suggest improvements. Focus on authentication, SQL injection, and input validation issues."
        },
        {
            "task": "Code Quality Improvement", 
            "prompt": "Analyze this code for best practices violations and suggest refactoring improvements. Focus on error handling, resource management, and code organization."
        },
        {
            "task": "Performance Optimization",
            "prompt": "Review this code for performance issues and suggest optimizations. Look for inefficient algorithms, unnecessary loops, and resource usage."
        },
        {
            "task": "Specific Function Refactor",
            "prompt": "Please refactor the JavaScript `processUserData` function to be more readable, efficient, and follow modern JavaScript best practices. Provide the improved code."
        },
        {
            "task": "Database Connection Fix",
            "prompt": "Fix the Go database connection function to properly handle errors, manage resources, and follow Go best practices. Show the corrected code."
        }
    ]
    
    print(f"\n🔧 Running {len(refactoring_tasks)} refactoring examples:")
    print("=" * 70)
    
    for i, task in enumerate(refactoring_tasks, 1):
        print(f"\n📝 TASK {i}/{len(refactoring_tasks)}: {task['task']}")
        print("-" * 50)
        
        send_chat_with_context(
            model_id=model_id,
            user_message=task['prompt'],
            context_content=context_content,
            context_description=f"code examples for {task['task'].lower()}",
            task_name=task['task']
        )
        
        if i < len(refactoring_tasks):
            try:
                input(f"\n⏸️  Press Enter to continue to task {i+1}...")
            except EOFError:
                print(f"\n⏭️  Continuing to task {i+1}...")
        print("=" * 70)

def interactive_context_mode(model_id):
    """Interactive mode where users can provide their own context and questions."""
    
    print(f"\n💬 Interactive Context Mode")
    print(f"🤖 Model: {model_id}")
    print("📋 Commands: 'quit'/'exit' to end, 'load' to load a new file, 'show' to show current context")
    print("-" * 70)
    
    current_context = None
    context_description = "user-provided context"
    
    while True:
        try:
            if not current_context:
                print(f"\n📄 No context loaded. Available options:")
                print(f"   1. Type 'load' to load a file")
                print(f"   2. Type 'paste' to paste context directly")
                print(f"   3. Type 'default' to use sample-code.md")
                
                user_input = input("\n👤 What would you like to do? ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'load':
                    file_path = input("📁 Enter file path: ").strip()
                    context = read_context_file(file_path)
                    if context:
                        current_context = context
                        context_description = f"content from {file_path}"
                        print(f"✅ Loaded {len(context)} characters from {file_path}")
                elif user_input.lower() == 'paste':
                    print("📝 Paste your context (press Ctrl+D when finished):")
                    lines = []
                    try:
                        while True:
                            line = input()
                            lines.append(line)
                    except EOFError:
                        current_context = '\n'.join(lines)
                        context_description = "pasted content"
                        print(f"✅ Loaded {len(current_context)} characters from pasted content")
                elif user_input.lower() == 'default':
                    context = read_context_file("sample-code.md")
                    if context:
                        current_context = context
                        context_description = "sample code examples"
                        print(f"✅ Loaded default sample code")
                else:
                    print("❌ Invalid option. Please try again.")
                continue
            
            user_input = input("\n👤 Ask something about the code (or 'load'/'show'/'quit'): ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'load':
                current_context = None
                continue
            elif user_input.lower() == 'show':
                if current_context:
                    print(f"\n📄 Current context ({len(current_context)} characters):")
                    print("-" * 50)
                    # Show first 500 characters
                    preview = current_context[:500]
                    if len(current_context) > 500:
                        preview += "... (truncated)"
                    print(preview)
                    print("-" * 50)
                else:
                    print("📄 No context currently loaded")
                continue
            elif not user_input:
                print("Please enter a question about the code")
                continue
            
            # Send the question with context
            send_chat_with_context(
                model_id=model_id,
                user_message=user_input,
                context_content=current_context,
                context_description=context_description,
                task_name=f"Interactive: {user_input[:30]}"
            )
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

def create_custom_context_example(model_id):
    """Allow users to create a custom context example."""
    
    print(f"\n📝 Custom Context Creator")
    print("Create your own code context for AI analysis")
    print("-" * 50)
    
    print("Choose context type:")
    print("1. Code snippet")
    print("2. Bug report with code")
    print("3. Performance issue description")
    print("4. Security audit request")
    
    choice = input("Enter choice (1-4): ").strip()
    
    templates = {
        "1": {
            "description": "code snippet for review",
            "prompt": "Please review this code snippet and suggest improvements for readability, performance, and best practices:"
        },
        "2": {
            "description": "bug report with code",
            "prompt": "This code has a bug. Please identify the issue and provide a fix:"
        },
        "3": {
            "description": "performance issue analysis", 
            "prompt": "This code is running slowly. Please analyze it for performance bottlenecks and suggest optimizations:"
        },
        "4": {
            "description": "security audit",
            "prompt": "Please perform a security audit on this code. Identify potential vulnerabilities and suggest fixes:"
        }
    }
    
    if choice in templates:
        template = templates[choice]
        print(f"\n📝 Enter your code for {template['description']}:")
        print("(Press Ctrl+D when finished)")
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            code_content = '\n'.join(lines)
            
            if code_content.strip():
                print(f"\n✅ Loaded {len(code_content)} characters")
                send_chat_with_context(
                    model_id=model_id,
                    user_message=template['prompt'],
                    context_content=code_content,
                    context_description=template['description'],
                    task_name=f"Custom: {template['description']}"
                )
            else:
                print("❌ No code provided")
    else:
        print("❌ Invalid choice")

def main():
    # Default model
    default_model = "anthropic::2024-10-22::claude-sonnet-4-latest"
    
    if len(sys.argv) > 1:
        model_id = sys.argv[1]
    else:
        model_id = default_model
        print(f"💡 Using default model: {model_id}")
    
    print("\n🔧 SOURCEGRAPH CODY API - MANUAL CONTEXT PASSING")
    print("=" * 70)
    print("This example shows how to manually provide context to the Cody API for:")
    print("   📝 Code review and refactoring suggestions")
    print("   🔍 Security vulnerability analysis")
    print("   ⚡ Performance optimization recommendations")
    print("   🐛 Bug identification and fixes")
    print("   📚 Best practices recommendations")
    print("=" * 70)
    print("\n📄 We'll use 'sample-code.md' as our context file containing example code")
    print("💾 All AI responses will be automatically saved to the 'responses/' directory")
    
    choice = input("\nChoose mode:\n1. 🔧 Run refactoring examples\n2. 💬 Interactive context mode\n3. 📝 Create custom context\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        run_refactoring_examples(model_id)
    elif choice == "2":
        interactive_context_mode(model_id)
    elif choice == "3":
        create_custom_context_example(model_id)
    else:
        print("Invalid choice. Running refactoring examples...")
        run_refactoring_examples(model_id)

if __name__ == "__main__":
    main()
