#!/usr/bin/env python3
"""
Sourcegraph Cody API - Context Search

This script demonstrates how to use Cody's context search to find relevant code
examples from repositories using natural language queries.

Usage:
    python 04-context.py
    
Make sure to set your environment variables in .env:
    SOURCEGRAPH_URL=https://sourcegraph.com
    SOURCEGRAPH_ACCESS_TOKEN=your_token_here
"""

import os
import json
import time
import requests
from dotenv import load_dotenv
from utils.file_utils import save_context_search_session_to_markdown

# Load environment variables from .env file
load_dotenv()

def search_code_context(query, repos, code_results=15, text_results=5, file_patterns=None, version="1.0", capture_details=False):
    """Search for code context using Cody's context API with optional detailed capture."""
    
    # Get configuration from environment
    base_url = os.getenv('SOURCEGRAPH_URL')
    access_token = os.getenv('SOURCEGRAPH_ACCESS_TOKEN')
    x_requested_with = os.getenv('SOURCEGRAPH_X_REQUESTED_WITH', 'cody-cookbook')
    
    if not base_url or not access_token:
        print("❌ Error: Please set SOURCEGRAPH_URL and SOURCEGRAPH_ACCESS_TOKEN in your .env file")
        return None
    
    # API endpoint
    url = f"{base_url}/.api/cody/context"
    
    # Headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'token {access_token}',
        'X-Requested-With': x_requested_with
    }
    
    # Request payload
    payload = {
        "query": query,
        "repos": repos,
        "codeResultsCount": code_results,
        "textResultsCount": text_results,
        "version": version
    }
    
    # Add file patterns if provided
    if file_patterns:
        payload["filePatterns"] = file_patterns
    
    # Initialize API details for tracking
    api_details = {
        'url': url,
        'headers': headers.copy(),
        'request_payload': payload.copy(),
        'query': query,
        'search_params': {
            'code_results': code_results,
            'text_results': text_results,
            'file_patterns': file_patterns,
            'version': version
        }
    }
    
    try:
        print(f"🔍 Searching for: '{query}'")
        print(f"📚 Repositories: {[repo['name'] for repo in repos]}")
        print(f"⚙️  Code results: {code_results}, Text results: {text_results}")
        if file_patterns:
            print(f"📁 File patterns: {file_patterns}")
        print("-" * 70)
        
        # Capture timing
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload)
        response_time = int((time.time() - start_time) * 1000)  # Convert to ms
        
        response.raise_for_status()
        
        data = response.json()
        results = data.get('results', [])
        
        # Capture response details if needed
        if capture_details:
            api_details['status_code'] = response.status_code
            api_details['response_time'] = response_time
            api_details['response_data'] = data.copy()
            api_details['results_count'] = len(results)
        
        print(f"✅ Found {len(results)} context results:")
        print("=" * 70)
        
        for i, result in enumerate(results, 1):
            blob = result.get('blob', {})
            repo_name = blob.get('repository', {}).get('name', 'Unknown')
            file_path = blob.get('path', 'Unknown')
            start_line = result.get('startLine', 0)
            end_line = result.get('endLine', 0)
            content = result.get('chunkContent', '')
            
            print(f"\n📄 Result {i}:")
            print(f"   Repository: {repo_name}")
            print(f"   File: {file_path}")
            print(f"   Lines: {start_line}-{end_line}")
            print(f"   Content:")
            
            # Display content with line numbers
            lines = content.split('\n')
            for j, line in enumerate(lines):
                line_num = start_line + j
                print(f"   {line_num:4d}: {line}")
            
            print("-" * 50)
        
        # Return both results and API details
        if capture_details:
            return results, api_details
        return results
        
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

def run_context_examples():
    """Run several examples of context search with session tracking."""
    
    # Example repositories - you may need to adjust these based on what's available
    example_repos = [
        {"name": "github.com/sourcegraph/cody"},
        {"name": "github.com/sourcegraph/sourcegraph"}
    ]
    
    examples = [
        {
            "query": "how to initialize a database connection?",
            "repos": example_repos,
            "file_patterns": [r"\.go$", r"\.ts$", r"\.py$"]
        },
        {
            "query": "authentication middleware implementation",
            "repos": example_repos,
            "file_patterns": [r"\.go$", r"\.ts$"]
        },
        {
            "query": "error handling patterns",
            "repos": example_repos,
            "code_results": 10,
            "text_results": 3
        },
        {
            "query": "unit test examples",
            "repos": example_repos,
            "file_patterns": [r".*test.*", r".*spec.*"]
        }
    ]
    
    print("🧪 Running context search examples:")
    print("=" * 70)
    
    search_history = []
    session_start_time = time.time()
    
    for i, example in enumerate(examples, 1):
        print(f"\n📝 Example {i}/{len(examples)}")
        
        # Perform search with details capture
        result = search_code_context(
            query=example["query"],
            repos=example["repos"],
            code_results=example.get("code_results", 5),
            text_results=example.get("text_results", 2),
            file_patterns=example.get("file_patterns"),
            capture_details=True
        )
        
        # Handle response (could be tuple or single value)
        if isinstance(result, tuple):
            results, api_details = result
        else:
            results = result
            api_details = {}
        
        # Store search details
        if results is not None:
            search_history.append({
                'query': example["query"],
                'results': results,
                'api_details': api_details,
                'search_params': {
                    'code_results': example.get("code_results", 5),
                    'text_results': example.get("text_results", 2),
                    'file_patterns': example.get("file_patterns"),
                    'version': "1.0"
                }
            })
        
        print("=" * 70)
    
    # Save session details
    if search_history:
        session_duration = time.time() - session_start_time
        session_duration_str = f"{int(session_duration // 60)}m {int(session_duration % 60)}s"
        
        session_metadata = {
            'mode': 'examples',
            'duration': session_duration_str,
            'default_repos': example_repos,
            'endpoint': f"{os.getenv('SOURCEGRAPH_URL')}/.api/cody/context"
        }
        
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        saved_path = save_context_search_session_to_markdown(
            search_history, 
            session_metadata, 
            script_name
        )
        
        if saved_path:
            print(f"\n📁 Context search session saved to: {saved_path}")

def interactive_context_search():
    """Run an interactive context search session with search history and session tracking."""
    print("🚀 Interactive Cody Context Search")
    print("Ask questions about code in natural language!")
    print("Type 'quit', 'exit', 'bye' to end, 'history' to see search history, or 'clear' to clear history")
    print("-" * 50)
    
    # Default repositories - modify these based on your needs
    default_repos = [
        {"name": "github.com/sourcegraph/cody"},
        {"name": "github.com/sourcegraph/sourcegraph"}
    ]
    
    print("📚 Default repositories:")
    for repo in default_repos:
        print(f"   - {repo['name']}")
    
    search_history = []  # Store previous searches with full details
    session_start_time = time.time()
    
    while True:
        try:
            user_input = input("\n🔍 Enter your search query: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'clear':
                search_history = []
                print("✅ Search history cleared")
                continue
            elif user_input.lower() == 'history':
                if search_history:
                    print("📜 Search History:")
                    for i, search in enumerate(search_history, 1):
                        result_count = len(search.get('results', []))
                        response_time = search.get('api_details', {}).get('response_time', 'N/A')
                        print(f"   {i}. {search['query']} (found {result_count} results, {response_time}ms)")
                else:
                    print("📜 No search history")
                continue
            elif not user_input:
                print("Please enter a search query")
                continue
            
            # Ask for optional file patterns
            patterns_input = input("📁 File patterns (optional, comma-separated): ").strip()
            file_patterns = None
            if patterns_input:
                file_patterns = [p.strip() for p in patterns_input.split(',')]
            
            # Ask for result counts
            try:
                code_count = input("📊 Number of code results (default 5): ").strip()
                code_count = int(code_count) if code_count else 5
                
                text_count = input("📊 Number of text results (default 3): ").strip()
                text_count = int(text_count) if text_count else 3
            except ValueError:
                print("Using default result counts")
                code_count, text_count = 5, 3
            
            # Perform the search with details capture
            result = search_code_context(
                query=user_input,
                repos=default_repos,
                code_results=code_count,
                text_results=text_count,
                file_patterns=file_patterns,
                capture_details=True
            )
            
            # Handle response (could be tuple or single value)
            if isinstance(result, tuple):
                results, api_details = result
            else:
                results = result
                api_details = {}
            
            # Add to search history with full details
            if results is not None:
                search_history.append({
                    "query": user_input,
                    "results": results,
                    "api_details": api_details,
                    "search_params": {
                        "code_results": code_count,
                        "text_results": text_count,
                        "file_patterns": file_patterns,
                        "version": "1.0"
                    }
                })
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
    
    # Save session details when interactive session ends
    if search_history:
        session_duration = time.time() - session_start_time
        session_duration_str = f"{int(session_duration // 60)}m {int(session_duration % 60)}s"
        
        session_metadata = {
            'mode': 'interactive',
            'duration': session_duration_str,
            'default_repos': default_repos,
            'endpoint': f"{os.getenv('SOURCEGRAPH_URL')}/.api/cody/context"
        }
        
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        saved_path = save_context_search_session_to_markdown(
            search_history, 
            session_metadata, 
            script_name
        )
        
        if saved_path:
            print(f"\n📁 Interactive search session saved to: {saved_path}")
    else:
        print("\n📝 No searches to save.")

def conversational_context_search():
    """Run a conversational context search that combines search results with chat and tracks everything."""
    print("🚀 Conversational Cody Context Search")
    print("Search for code and ask questions about the results!")
    print("Type 'quit', 'exit', 'bye' to end, 'search' to perform a new search, or 'clear' to clear context")
    print("-" * 70)
    
    # Default repositories - modify these based on your needs
    default_repos = [
        {"name": "github.com/sourcegraph/cody"},
        {"name": "github.com/sourcegraph/sourcegraph"}
    ]
    
    print("📚 Default repositories:")
    for repo in default_repos:
        print(f"   - {repo['name']}")
    
    current_context = []  # Store current search results as context
    conversation_history = []  # Store conversation
    search_history = []  # Store all searches with full details
    session_start_time = time.time()
    
    while True:
        try:
            if not current_context:
                print("\n🔍 First, let's search for some code context...")
                search_query = input("Enter your search query: ").strip()
                
                if search_query.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                elif not search_query:
                    print("Please enter a search query")
                    continue
                
                # Perform context search with details capture
                result = search_code_context(
                    query=search_query,
                    repos=default_repos,
                    code_results=5,
                    text_results=3,
                    capture_details=True
                )
                
                # Handle response (could be tuple or single value)
                if isinstance(result, tuple):
                    results, api_details = result
                else:
                    results = result
                    api_details = {}
                
                if results:
                    current_context = results
                    
                    # Store search details
                    search_history.append({
                        'query': search_query,
                        'results': results,
                        'api_details': api_details,
                        'search_params': {
                            'code_results': 5,
                            'text_results': 3,
                            'file_patterns': None,
                            'version': "1.0"
                        },
                        'used_for_conversation': True
                    })
                    
                    # Add search results as context to conversation
                    context_summary = f"Search results for '{search_query}':\n"
                    for i, result in enumerate(results[:3], 1):  # Limit context to first 3 results
                        blob = result.get('blob', {})
                        repo_name = blob.get('repository', {}).get('name', 'Unknown')
                        file_path = blob.get('path', 'Unknown')
                        content = result.get('chunkContent', '')[:200] + "..."  # Truncate content
                        context_summary += f"{i}. {repo_name}/{file_path}: {content}\n"
                    
                    conversation_history.append({
                        "role": "system",
                        "content": f"You are helping analyze code search results. Here are the search results:\n{context_summary}"
                    })
                    
                    print(f"\n💬 Now you can ask questions about these {len(results)} search results!")
                else:
                    print("No results found. Try a different search query.")
                    continue
            
            user_input = input("\n👤 Ask about the code (or type 'search' for new search): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'search':
                current_context = []
                # Keep conversation history for context but mark new search
                print("✅ Starting new search...")
                continue
            elif user_input.lower() == 'clear':
                conversation_history = [msg for msg in conversation_history if msg.get('role') == 'system']
                print("✅ Conversation cleared (keeping search context)")
                continue
            elif not user_input:
                print("Please enter a question or 'search' for new search")
                continue
            
            # Add user question to conversation
            conversation_history.append({
                "role": "user", 
                "content": user_input
            })
            
            print("💭 This would send the conversation to a chat model to analyze the code context...")
            print(f"   Conversation has {len(conversation_history)} messages")
            print(f"   Current context: {len(current_context)} search results")
            print("   (Note: Actual chat integration would require a chat model setup)")
            
            # Simulate assistant response for demonstration
            conversation_history.append({
                "role": "assistant",
                "content": f"I would analyze the code context and provide insights about: '{user_input}'"
            })
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
    
    # Save both search session and conversation details when conversational session ends
    if search_history or conversation_history:
        session_duration = time.time() - session_start_time
        session_duration_str = f"{int(session_duration // 60)}m {int(session_duration % 60)}s"
        
        # Save context search session
        if search_history:
            session_metadata = {
                'mode': 'conversational',
                'duration': session_duration_str,
                'default_repos': default_repos,
                'endpoint': f"{os.getenv('SOURCEGRAPH_URL')}/.api/cody/context",
                'conversation_messages': len(conversation_history),
                'includes_conversation': True,
                'conversation_history': conversation_history
            }
            
            script_name = os.path.splitext(os.path.basename(__file__))[0]
            saved_path = save_context_search_session_to_markdown(
                search_history, 
                session_metadata, 
                script_name
            )
            
            if saved_path:
                print(f"\n📁 Conversational search session saved to: {saved_path}")
        
        # Also save conversation history separately if needed
        if conversation_history and len(conversation_history) > 1:  # More than just system message
            print(f"\n💬 Conversation included {len(conversation_history)} messages")
            print("   (Conversation details are included in the search session file)")
    else:
        print("\n📝 No searches or conversations to save.")

def main():
    print("🔍 Sourcegraph Cody Context Search Examples")
    print("This tool helps you find relevant code using natural language queries")
    
    choice = input("\nChoose mode:\n1. Run examples\n2. Interactive search\n3. Conversational search\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        run_context_examples()
    elif choice == "2":
        interactive_context_search()
    elif choice == "3":
        conversational_context_search()
    else:
        print("Invalid choice. Running examples...")
        run_context_examples()

if __name__ == "__main__":
    main()
