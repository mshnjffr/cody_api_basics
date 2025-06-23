"""
File utilities for saving API responses and data.

This module provides reusable functions for saving various types of data
from the Cody API to organized files with timestamps and metadata.
"""

import os
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional, Union


def save_models_to_csv(models_data: List[Dict[str, Any]], script_name: str = "models") -> Optional[str]:
    """
    Save models data to a CSV file with timestamp.
    
    Args:
        models_data: List of model dictionaries from the API
        script_name: Name to include in the filename
        
    Returns:
        str: File path if successful, None if failed
    """
    responses_dir = _ensure_responses_directory()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{script_name}.csv"
    filepath = os.path.join(responses_dir, filename)
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            # Define CSV headers
            fieldnames = ['model_id', 'owner', 'created', 'object_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write model data
            for model in models_data:
                writer.writerow({
                    'model_id': model.get('id', 'N/A'),
                    'owner': model.get('owned_by', 'N/A'),
                    'created': model.get('created', 0),
                    'object_type': model.get('object', 'model')
                })
        
        print(f"💾 Models CSV saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving models to CSV: {e}")
        return None


def save_models_to_markdown(models_data: List[Dict[str, Any]], script_name: str = "models") -> Optional[str]:
    """
    Save models data to a Markdown file with timestamp.
    
    Args:
        models_data: List of model dictionaries from the API
        script_name: Name to include in the filename
        
    Returns:
        str: File path if successful, None if failed
    """
    responses_dir = _ensure_responses_directory()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{script_name}.md"
    filepath = os.path.join(responses_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            # Write header with metadata
            file.write(f"# Available Models: {script_name}\n\n")
            file.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            file.write(f"**Total Models Found:** {len(models_data)}\n\n")
            file.write("---\n\n")
            
            # Write models table
            file.write("## Available Models\n\n")
            file.write("| Model ID | Owner | Created | Object Type |\n")
            file.write("|----------|-------|---------|-------------|\n")
            
            for model in models_data:
                model_id = model.get('id', 'N/A')
                owner = model.get('owned_by', 'N/A')
                created = model.get('created', 0)
                object_type = model.get('object', 'model')
                file.write(f"| {model_id} | {owner} | {created} | {object_type} |\n")
            
            file.write(f"\n## Usage Examples\n\n")
            file.write("Copy any model ID from above to use in other scripts:\n\n")
            file.write("```bash\n")
            file.write("# Get model details\n")
            file.write("python 01-modelinstance.py MODEL_ID\n\n")
            file.write("# Start chat with specific model\n")
            file.write("python 02-chat.py MODEL_ID\n\n")
            file.write("# Use with tools\n")
            file.write("python 03-tools.py MODEL_ID\n\n")
            file.write("# Use with manual context\n")
            file.write("python 05-manual-context.py MODEL_ID\n")
            file.write("```\n")
            
            # Add model ID format explanation
            file.write(f"\n## Model ID Format\n\n")
            file.write("Model IDs follow the pattern: `${{ProviderID}}::${{APIVersionID}}::${{ModelID}}`\n\n")
            file.write("Examples:\n")
            file.write("- `anthropic::2024-10-22::claude-sonnet-4-latest`\n")
            file.write("- `openai::2024-02-01::gpt-4o`\n")
            file.write("- `mistral::v1::mixtral-8x7b-instruct`\n")
        
        print(f"💾 Models markdown saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving models to markdown: {e}")
        return None


def save_model_instance_to_markdown(model_data: Dict[str, Any], script_name: str = "model-instance") -> Optional[str]:
    """
    Save single model instance data to a Markdown file with timestamp.
    
    Args:
        model_data: Single model dictionary from the API
        script_name: Name to include in the filename
        
    Returns:
        str: File path if successful, None if failed
    """
    responses_dir = _ensure_responses_directory()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_id_safe = model_data.get('id', 'unknown').replace('::', '_').replace('/', '_')
    filename = f"{timestamp}_{script_name}_{model_id_safe}.md"
    filepath = os.path.join(responses_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            # Write header with metadata
            file.write(f"# Model Instance Details: {model_data.get('id', 'Unknown')}\n\n")
            file.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            file.write(f"**Script:** {script_name}\n\n")
            file.write("---\n\n")
            
            # Write model details
            file.write("## Model Information\n\n")
            file.write(f"- **Model ID:** `{model_data.get('id', 'N/A')}`\n")
            file.write(f"- **Object Type:** `{model_data.get('object', 'N/A')}`\n")
            file.write(f"- **Owner:** `{model_data.get('owned_by', 'N/A')}`\n")
            file.write(f"- **Created:** `{model_data.get('created', 'N/A')}`\n\n")
            
            # Add usage examples
            file.write("## Usage Examples\n\n")
            file.write(f"Use this model ID in other scripts:\n\n")
            file.write("```bash\n")
            file.write(f"# Start interactive chat\n")
            file.write(f"python 02-chat.py {model_data.get('id', 'MODEL_ID')}\n\n")
            file.write(f"# Use with function calling\n")
            file.write(f"python 03-tools.py {model_data.get('id', 'MODEL_ID')}\n\n")
            file.write(f"# Use with manual context\n")
            file.write(f"python 05-manual-context.py {model_data.get('id', 'MODEL_ID')}\n")
            file.write("```\n\n")
            
            # Add model ID breakdown
            model_id = model_data.get('id', '')
            if '::' in model_id:
                parts = model_id.split('::')
                if len(parts) == 3:
                    file.write("## Model ID Breakdown\n\n")
                    file.write(f"- **Provider:** `{parts[0]}`\n")
                    file.write(f"- **API Version:** `{parts[1]}`\n")
                    file.write(f"- **Model Name:** `{parts[2]}`\n\n")
            
            # Add raw JSON data
            file.write("## Raw API Response\n\n")
            file.write("```json\n")
            import json
            file.write(json.dumps(model_data, indent=2, ensure_ascii=False))
            file.write("\n```\n")
        
        print(f"💾 Model instance saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving model instance to markdown: {e}")
        return None


def _ensure_responses_directory() -> str:
    """
    Ensure responses directory exists (DRY principle - shared helper).
    
    Returns:
        str: Path to responses directory
    """
    responses_dir = "responses"
    if not os.path.exists(responses_dir):
        os.makedirs(responses_dir)
        print(f"📁 Created responses directory: {responses_dir}")
    return responses_dir


def save_chat_session_to_markdown(
    conversation_history: List[Dict[str, str]],
    api_calls_history: List[Dict[str, Any]],
    session_metadata: Dict[str, Any],
    script_name: str = "chat-session"
) -> Optional[str]:
    """
    Save complete chat session with API details to a Markdown file.
    
    Args:
        conversation_history: List of messages in the conversation
        api_calls_history: List of API call details for each interaction
        session_metadata: Session settings and metadata
        script_name: Name to include in the filename
        
    Returns:
        str: File path if successful, None if failed
    """
    responses_dir = _ensure_responses_directory()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_safe = session_metadata.get('model_id', 'unknown').replace('::', '_').replace('/', '_')
    filename = f"{timestamp}_{script_name}_{model_safe}.md"
    filepath = os.path.join(responses_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            # Write header with metadata
            file.write(f"# Chat Session: {session_metadata.get('model_id', 'Unknown Model')}\n\n")
            file.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            file.write(f"**Script:** {script_name}\n\n")
            file.write(f"**Session Duration:** {session_metadata.get('duration', 'N/A')}\n\n")
            file.write("---\n\n")
            
            # Write session settings
            file.write("## Session Settings\n\n")
            file.write(f"- **Model ID:** `{session_metadata.get('model_id', 'N/A')}`\n")
            file.write(f"- **Temperature:** `{session_metadata.get('temperature', 'N/A')}`\n")
            file.write(f"- **Max Tokens:** `{session_metadata.get('max_tokens', 'N/A')}`\n")
            file.write(f"- **Total Messages:** `{len(conversation_history)}`\n")
            file.write(f"- **Total API Calls:** `{session_metadata.get('api_calls_count', 'N/A')}`\n\n")
            
            # Write conversation with interleaved API details
            file.write("## Conversation Flow\n\n")
            
            # Group user messages with their corresponding API calls
            user_message_count = 0
            for i, message in enumerate(conversation_history):
                role = message.get('role', 'unknown')
                content = message.get('content', '')
                
                if role == "user":
                    user_message_count += 1
                    file.write(f"### {user_message_count}. 👤 User Message\n\n")
                    file.write(f"{content}\n\n")
                    
                    # Find corresponding API call for this user message
                    api_call_index = user_message_count - 1
                    if api_call_index < len(api_calls_history):
                        api_call = api_calls_history[api_call_index]
                        
                        file.write(f"#### 🔄 API Request #{user_message_count}\n\n")
                        file.write(f"- **Endpoint:** `{api_call.get('url', 'N/A')}`\n")
                        file.write(f"- **Method:** `POST`\n")
                        file.write(f"- **Status Code:** `{api_call.get('status_code', 'N/A')}`\n")
                        file.write(f"- **Response Time:** `{api_call.get('response_time', 'N/A')}ms`\n\n")
                        
                        # Show headers (redacted)
                        file.write("**Headers:**\n")
                        for header, value in api_call.get('headers', {}).items():
                            if 'token' in header.lower() or 'authorization' in header.lower():
                                value = '[REDACTED]'
                            file.write(f"- `{header}: {value}`\n")
                        file.write("\n")
                        
                        # Show the complete request payload that was sent
                        file.write("**Complete Request Payload:**\n\n")
                        file.write("```json\n")
                        import json
                        
                        # Show the actual payload that was sent to the API
                        request_payload = api_call.get('request_payload', {})
                        file.write(json.dumps(request_payload, indent=2, ensure_ascii=False))
                        file.write("\n```\n\n")
                        
                elif role == "assistant":
                    file.write(f"#### 🤖 Assistant Response\n\n")
                    file.write(f"{content}\n\n")
                    
                    # Show token usage if available
                    api_call_index = user_message_count - 1
                    if api_call_index < len(api_calls_history):
                        api_call = api_calls_history[api_call_index]
                        usage = api_call.get('usage', {})
                        if usage:
                            file.write("**Token Usage:**\n")
                            file.write(f"- Prompt Tokens: `{usage.get('prompt_tokens', 'N/A')}`\n")
                            file.write(f"- Completion Tokens: `{usage.get('completion_tokens', 'N/A')}`\n")
                            file.write(f"- Total Tokens: `{usage.get('total_tokens', 'N/A')}`\n\n")
                    
                    file.write("---\n\n")
            
            # Add usage examples
            file.write("## Continue This Session\n\n")
            file.write("To continue with this model:\n\n")
            file.write("```bash\n")
            file.write(f"python 02-chat.py {session_metadata.get('model_id', 'MODEL_ID')}\n")
            file.write("```\n")
        
        print(f"💾 Chat session saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving chat session: {e}")
        return None


def save_tool_calling_session_to_markdown(
    session_steps: List[Dict[str, Any]],
    session_metadata: Dict[str, Any],
    script_name: str = "tool-calling-session"
) -> Optional[str]:
    """
    Save complete tool calling session with API details to a Markdown file.
    
    Args:
        session_steps: List of session steps with details
        session_metadata: Session settings and metadata
        script_name: Name to include in the filename
        
    Returns:
        str: File path if successful, None if failed
    """
    responses_dir = _ensure_responses_directory()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_safe = session_metadata.get('model_id', 'unknown').replace('::', '_').replace('/', '_')
    filename = f"{timestamp}_{script_name}_{model_safe}.md"
    filepath = os.path.join(responses_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            # Write header with metadata
            file.write(f"# Tool Calling Session: {session_metadata.get('model_id', 'Unknown Model')}\n\n")
            file.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            file.write(f"**Script:** {script_name}\n\n")
            file.write(f"**Session Duration:** {session_metadata.get('duration', 'N/A')}\n\n")
            file.write("---\n\n")
            
            # Write session overview
            file.write("## Session Overview\n\n")
            file.write(f"- **Model ID:** `{session_metadata.get('model_id', 'N/A')}`\n")
            file.write(f"- **Temperature:** `{session_metadata.get('temperature', 'N/A')}`\n")
            file.write(f"- **Max Tokens:** `{session_metadata.get('max_tokens', 'N/A')}`\n")
            file.write(f"- **Total API Calls:** `{session_metadata.get('total_api_calls', 'N/A')}`\n")
            file.write(f"- **Total Tool Calls:** `{session_metadata.get('total_tool_calls', 'N/A')}`\n")
            file.write(f"- **User Query:** `{session_metadata.get('user_query', 'N/A')}`\n\n")
            
            # Write available tools
            available_tools = session_metadata.get('available_tools', [])
            if available_tools:
                file.write("## Available Tools\n\n")
                for tool in available_tools:
                    file.write(f"- **{tool.get('name', 'Unknown')}:** {tool.get('description', 'No description')}\n")
                file.write("\n")
            
            # Write step-by-step tool calling flow
            file.write("## Tool Calling Flow\n\n")
            
            for step in session_steps:
                step_number = step.get('step_number', 'N/A')
                step_type = step.get('step_type', 'unknown')
                
                if step_type == "initial_request":
                    file.write(f"### Step {step_number}: 📤 Initial AI Request\n\n")
                    file.write(f"**User Query:** {step.get('user_query', 'N/A')}\n\n")
                    
                    # API call details
                    api_details = step.get('api_details', {})
                    if api_details:
                        file.write("#### 🔄 API Call Details\n\n")
                        file.write(f"- **Endpoint:** `{api_details.get('url', 'N/A')}`\n")
                        file.write(f"- **Method:** `POST`\n")
                        file.write(f"- **Status Code:** `{api_details.get('status_code', 'N/A')}`\n")
                        file.write(f"- **Response Time:** `{api_details.get('response_time', 'N/A')}ms`\n\n")
                        
                        # Show headers (redacted)
                        file.write("**Headers:**\n")
                        for header, value in api_details.get('headers', {}).items():
                            if 'token' in header.lower() or 'authorization' in header.lower():
                                value = '[REDACTED]'
                            file.write(f"- `{header}: {value}`\n")
                        file.write("\n")
                        
                        # Show complete request payload
                        file.write("**Complete Request Payload:**\n\n")
                        file.write("```json\n")
                        import json
                        request_payload = api_details.get('request_payload', {})
                        file.write(json.dumps(request_payload, indent=2, ensure_ascii=False))
                        file.write("\n```\n\n")
                        
                        # Show complete response payload
                        file.write("**Complete Response Payload:**\n\n")
                        file.write("```json\n")
                        response_payload = api_details.get('response_data', {})
                        file.write(json.dumps(response_payload, indent=2, ensure_ascii=False))
                        file.write("\n```\n\n")
                    
                elif step_type == "tool_execution":
                    file.write(f"### Step {step_number}: 🔧 Tool Execution\n\n")
                    
                    tool_calls = step.get('tool_calls', [])
                    for i, tool_call in enumerate(tool_calls, 1):
                        file.write(f"#### Tool Call #{i}: {tool_call.get('function_name', 'Unknown')}\n\n")
                        file.write(f"- **Function:** `{tool_call.get('function_name', 'N/A')}`\n")
                        file.write(f"- **Call ID:** `{tool_call.get('call_id', 'N/A')}`\n\n")
                        
                        # Show function arguments
                        file.write("**Function Arguments:**\n\n")
                        file.write("```json\n")
                        file.write(json.dumps(tool_call.get('function_args', {}), indent=2, ensure_ascii=False))
                        file.write("\n```\n\n")
                        
                        # Show function result
                        file.write("**Function Result:**\n\n")
                        file.write("```json\n")
                        result = tool_call.get('function_result', '')
                        try:
                            # Try to parse as JSON for pretty printing
                            if isinstance(result, str):
                                result_json = json.loads(result)
                                file.write(json.dumps(result_json, indent=2, ensure_ascii=False))
                            else:
                                file.write(json.dumps(result, indent=2, ensure_ascii=False))
                        except (json.JSONDecodeError, TypeError):
                            file.write(str(result))
                        file.write("\n```\n\n")
                    
                elif step_type == "final_response":
                    file.write(f"### Step {step_number}: 🎯 Final AI Response\n\n")
                    
                    # API call details for final response
                    api_details = step.get('api_details', {})
                    if api_details:
                        file.write("#### 🔄 API Call Details\n\n")
                        file.write(f"- **Endpoint:** `{api_details.get('url', 'N/A')}`\n")
                        file.write(f"- **Method:** `POST`\n")
                        file.write(f"- **Status Code:** `{api_details.get('status_code', 'N/A')}`\n")
                        file.write(f"- **Response Time:** `{api_details.get('response_time', 'N/A')}ms`\n\n")
                        
                        # Show token usage if available
                        usage = api_details.get('usage', {})
                        if usage:
                            file.write("**Token Usage:**\n")
                            file.write(f"- Prompt Tokens: `{usage.get('prompt_tokens', 'N/A')}`\n")
                            file.write(f"- Completion Tokens: `{usage.get('completion_tokens', 'N/A')}`\n")
                            file.write(f"- Total Tokens: `{usage.get('total_tokens', 'N/A')}`\n\n")
                        
                        # Show complete final response payload
                        file.write("**Complete Response Payload:**\n\n")
                        file.write("```json\n")
                        response_payload = api_details.get('response_data', {})
                        file.write(json.dumps(response_payload, indent=2, ensure_ascii=False))
                        file.write("\n```\n\n")
                    
                    # Show final AI response content
                    ai_response = step.get('ai_response', '')
                    if ai_response:
                        file.write("#### 🤖 Final AI Response Content\n\n")
                        file.write(f"{ai_response}\n\n")
                
                file.write("---\n\n")
            
            # Write complete conversation context
            complete_conversation = session_metadata.get('complete_conversation', [])
            if complete_conversation:
                file.write("## Complete Conversation Context\n\n")
                file.write("This shows the full conversation that was built up during the tool calling process:\n\n")
                file.write("```json\n")
                file.write(json.dumps(complete_conversation, indent=2, ensure_ascii=False))
                file.write("\n```\n\n")
            
            # Add usage examples
            file.write("## Continue With This Model\n\n")
            file.write("To use this model for more tool calling:\n\n")
            file.write("```bash\n")
            file.write(f"python 03-tools.py {session_metadata.get('model_id', 'MODEL_ID')}\n")
            file.write("```\n")
        
        print(f"💾 Tool calling session saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving tool calling session: {e}")
        return None


def save_data_to_json(data: Any, script_name: str = "data", pretty: bool = True) -> Optional[str]:
    """
    Save any data to a JSON file with timestamp.
    
    Args:
        data: Any JSON-serializable data
        script_name: Name to include in the filename
        pretty: Whether to pretty-print the JSON
        
    Returns:
        str: File path if successful, None if failed
    """
    responses_dir = _ensure_responses_directory()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{script_name}.json"
    filepath = os.path.join(responses_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            if pretty:
                import json
                json.dump(data, file, indent=2, ensure_ascii=False)
            else:
                import json
                json.dump(data, file, ensure_ascii=False)
        
        print(f"💾 JSON data saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving data to JSON: {e}")
        return None


def save_context_search_session_to_markdown(
    search_history: List[Dict[str, Any]],
    session_metadata: Dict[str, Any],
    script_name: str = "context-search-session"
) -> Optional[str]:
    """
    Save complete context search session with API details to a Markdown file.
    
    Args:
        search_history: List of search queries with their results and API details
        session_metadata: Session settings and metadata
        script_name: Name to include in the filename
        
    Returns:
        str: File path if successful, None if failed
    """
    responses_dir = _ensure_responses_directory()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode = session_metadata.get('mode', 'unknown')
    filename = f"{timestamp}_{script_name}_{mode}.md"
    filepath = os.path.join(responses_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            # Write header with metadata
            file.write(f"# Context Search Session: {session_metadata.get('mode', 'Unknown Mode')}\n\n")
            file.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            file.write(f"**Script:** {script_name}\n\n")
            file.write(f"**Session Duration:** {session_metadata.get('duration', 'N/A')}\n\n")
            file.write("---\n\n")
            
            # Write session settings
            file.write("## Session Settings\n\n")
            file.write(f"- **Mode:** `{session_metadata.get('mode', 'N/A')}`\n")
            file.write(f"- **Total Searches:** `{len(search_history)}`\n")
            file.write(f"- **Default Repositories:**\n")
            for repo in session_metadata.get('default_repos', []):
                file.write(f"  - `{repo.get('name', 'Unknown')}`\n")
            file.write(f"- **API Endpoint:** `{session_metadata.get('endpoint', 'N/A')}`\n\n")
            
            # Write performance summary
            if search_history:
                total_results = sum(len(search.get('results', [])) for search in search_history)
                total_time = sum(search.get('api_details', {}).get('response_time', 0) for search in search_history)
                avg_time = total_time / len(search_history) if search_history else 0
                
                file.write("## Performance Summary\n\n")
                file.write(f"- **Total Results Found:** `{total_results}`\n")
                file.write(f"- **Total API Response Time:** `{total_time}ms`\n")
                file.write(f"- **Average Response Time:** `{avg_time:.1f}ms`\n")
                file.write(f"- **Fastest Query:** `{min((s.get('api_details', {}).get('response_time', 0) for s in search_history), default=0)}ms`\n")
                file.write(f"- **Slowest Query:** `{max((s.get('api_details', {}).get('response_time', 0) for s in search_history), default=0)}ms`\n\n")
            
            # Write search history
            file.write("## Search History & Results\n\n")
            
            for i, search in enumerate(search_history, 1):
                query = search.get('query', 'Unknown')
                results = search.get('results', [])
                api_details = search.get('api_details', {})
                search_params = search.get('search_params', {})
                
                file.write(f"### {i}. Search: \"{query}\"\n\n")
                
                # Search parameters
                file.write("#### 🔍 Search Parameters\n\n")
                file.write(f"- **Query:** `{query}`\n")
                file.write(f"- **Code Results:** `{search_params.get('code_results', 'N/A')}`\n")
                file.write(f"- **Text Results:** `{search_params.get('text_results', 'N/A')}`\n")
                file.write(f"- **File Patterns:** `{search_params.get('file_patterns', 'None')}`\n")
                file.write(f"- **Version:** `{search_params.get('version', 'N/A')}`\n\n")
                
                # API call details
                file.write("#### 🔄 API Call Details\n\n")
                file.write(f"- **Status Code:** `{api_details.get('status_code', 'N/A')}`\n")
                file.write(f"- **Response Time:** `{api_details.get('response_time', 'N/A')}ms`\n")
                file.write(f"- **Results Found:** `{len(results)}`\n\n")
                
                # Show headers (redacted)
                if api_details.get('headers'):
                    file.write("**Headers:**\n")
                    for header, value in api_details.get('headers', {}).items():
                        if 'token' in header.lower() or 'authorization' in header.lower():
                            value = '[REDACTED]'
                        file.write(f"- `{header}: {value}`\n")
                    file.write("\n")
                
                # Show complete request payload
                if api_details.get('request_payload'):
                    file.write("**Complete Request Payload:**\n\n")
                    file.write("```json\n")
                    import json
                    file.write(json.dumps(api_details.get('request_payload', {}), indent=2, ensure_ascii=False))
                    file.write("\n```\n\n")
                
                # Search results
                if results:
                    file.write(f"#### 📄 Search Results ({len(results)} found)\n\n")
                    
                    for j, result in enumerate(results, 1):
                        blob = result.get('blob', {})
                        repo_name = blob.get('repository', {}).get('name', 'Unknown')
                        file_path = blob.get('path', 'Unknown')
                        start_line = result.get('startLine', 0)
                        end_line = result.get('endLine', 0)
                        content = result.get('chunkContent', '')
                        
                        file.write(f"**Result {j}:**\n\n")
                        file.write(f"- **Repository:** `{repo_name}`\n")
                        file.write(f"- **File:** `{file_path}`\n")
                        file.write(f"- **Lines:** `{start_line}-{end_line}`\n\n")
                        
                        # Show code content
                        if content:
                            file.write("**Code:**\n\n")
                            file.write("```\n")
                            # Add line numbers to content
                            lines = content.split('\n')
                            for k, line in enumerate(lines):
                                line_num = start_line + k
                                file.write(f"{line_num:4d}: {line}\n")
                            file.write("```\n\n")
                        
                        file.write("---\n\n")
                else:
                    file.write("#### 📄 Search Results\n\n")
                    file.write("*No results found for this query.*\n\n")
                
                file.write("=" * 70 + "\n\n")
            
            # Add conversation details if this was a conversational session
            if session_metadata.get('includes_conversation') and session_metadata.get('conversation_history'):
                conversation_history = session_metadata.get('conversation_history', [])
                file.write("## Conversation History\n\n")
                file.write(f"This was a conversational session with {len(conversation_history)} messages.\n\n")
                
                for i, message in enumerate(conversation_history, 1):
                    role = message.get('role', 'unknown')
                    content = message.get('content', '')
                    
                    if role == "system":
                        file.write(f"### {i}. 🔧 System Context\n\n")
                        file.write(f"{content}\n\n")
                    elif role == "user":
                        file.write(f"### {i}. 👤 User Question\n\n")
                        file.write(f"{content}\n\n")
                    elif role == "assistant":
                        file.write(f"### {i}. 🤖 Assistant Response\n\n")
                        file.write(f"{content}\n\n")
                
                file.write("---\n\n")
            
            # Add usage examples
            file.write("## Continue Searching\n\n")
            file.write("To continue searching:\n\n")
            file.write("```bash\n")
            file.write("python 04-context.py\n")
            file.write("```\n\n")
            
            # Add raw API response data if needed
            if search_history and session_metadata.get('include_raw_data', False):
                file.write("## Raw API Response Data\n\n")
                file.write("```json\n")
                import json
                file.write(json.dumps(search_history, indent=2, ensure_ascii=False))
                file.write("\n```\n")
        
        print(f"💾 Context search session saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving context search session: {e}")
        return None


def save_manual_context_session_to_markdown(
    tasks_or_interactions: List[Dict[str, Any]],
    api_calls_history: List[Dict[str, Any]],
    session_metadata: Dict[str, Any],
    script_name: str = "manual-context-session"
) -> Optional[str]:
    """
    Save complete manual context session with API details to a Markdown file.
    
    Args:
        tasks_or_interactions: List of tasks (for refactoring) or interactions (for interactive)
        api_calls_history: List of API call details for each request
        session_metadata: Session settings and metadata including mode
        script_name: Name to include in the filename
        
    Returns:
        str: File path if successful, None if failed
    """
    responses_dir = _ensure_responses_directory()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_safe = session_metadata.get('model_id', 'unknown').replace('::', '_').replace('/', '_')
    mode = session_metadata.get('mode', 'unknown')
    filename = f"{timestamp}_{script_name}_{mode}_{model_safe}.md"
    filepath = os.path.join(responses_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            # Write header with metadata
            file.write(f"# Manual Context Session: {session_metadata.get('model_id', 'Unknown Model')}\n\n")
            file.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            file.write(f"**Script:** {script_name}\n\n")
            file.write(f"**Mode:** {session_metadata.get('mode', 'N/A')}\n\n")
            file.write(f"**Session Duration:** {session_metadata.get('duration', 'N/A')}\n\n")
            file.write("---\n\n")
            
            # Write session settings
            file.write("## Session Settings\n\n")
            file.write(f"- **Model ID:** `{session_metadata.get('model_id', 'N/A')}`\n")
            file.write(f"- **Mode:** `{session_metadata.get('mode', 'N/A')}`\n")
            file.write(f"- **Duration:** `{session_metadata.get('duration', 'N/A')}`\n")
            file.write(f"- **Total API Calls:** `{session_metadata.get('api_calls_count', 'N/A')}`\n")
            
            # Mode-specific metadata
            mode = session_metadata.get('mode', '')
            if mode == 'refactoring_examples':
                file.write(f"- **Total Tasks:** `{session_metadata.get('total_tasks', 'N/A')}`\n")
                file.write(f"- **Completed Tasks:** `{session_metadata.get('completed_tasks', 'N/A')}`\n")
                context_metadata = session_metadata.get('context_metadata', {})
                file.write(f"- **Context File:** `{context_metadata.get('context_file', 'N/A')}`\n")
                file.write(f"- **Context Size:** `{context_metadata.get('context_size', 'N/A')} characters`\n")
            elif mode == 'interactive_context':
                file.write(f"- **Total Interactions:** `{session_metadata.get('total_interactions', 'N/A')}`\n")
                file.write(f"- **Context Switches:** `{session_metadata.get('total_context_switches', 'N/A')}`\n")
            elif mode == 'custom_context':
                file.write(f"- **Custom Type:** `{session_metadata.get('custom_type', 'N/A')}`\n")
                context_metadata = session_metadata.get('context_metadata', {})
                file.write(f"- **Context Size:** `{context_metadata.get('context_size', 'N/A')} characters`\n")
            
            file.write("\n")
            
            # Write context switches for interactive mode
            if mode == 'interactive_context' and 'context_switches' in session_metadata:
                file.write("## Context Management\n\n")
                context_switches = session_metadata['context_switches']
                if context_switches:
                    file.write("### Context Switches\n\n")
                    for i, switch in enumerate(context_switches, 1):
                        file.write(f"#### {i}. {switch.get('action', 'Unknown Action')} - {switch.get('timestamp', 'N/A')}\n\n")
                        file.write(f"- **Action:** `{switch.get('action', 'N/A')}`\n")
                        if 'file_path' in switch:
                            file.write(f"- **File Path:** `{switch.get('file_path', 'N/A')}`\n")
                        file.write(f"- **Context Size:** `{switch.get('context_size', 'N/A')} characters`\n")
                        file.write(f"- **Description:** {switch.get('description', 'N/A')}\n\n")
                else:
                    file.write("No context switches recorded.\n\n")
            
            # Write tasks/interactions with API details
            if mode == 'refactoring_examples':
                file.write("## Refactoring Tasks\n\n")
                _write_refactoring_tasks(file, tasks_or_interactions, api_calls_history)
            elif mode == 'interactive_context':
                file.write("## Interactive Session\n\n")
                _write_interactive_session(file, tasks_or_interactions, api_calls_history)
            elif mode == 'custom_context':
                file.write("## Custom Context Analysis\n\n")
                _write_custom_context_analysis(file, tasks_or_interactions, api_calls_history)
            
            # Add usage examples
            file.write("## Continue Working\n\n")
            file.write("To continue with this model:\n\n")
            file.write("```bash\n")
            file.write(f"python 05-manual-context.py {session_metadata.get('model_id', 'MODEL_ID')}\n")
            file.write("```\n")
        
        print(f"💾 Manual context session saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving manual context session: {e}")
        return None


def _write_refactoring_tasks(file, tasks: List[Dict[str, Any]], api_calls_history: List[Dict[str, Any]]):
    """Helper function to write refactoring tasks section."""
    for i, task in enumerate(tasks):
        task_num = task.get('task_number', i + 1)
        file.write(f"### {task_num}. {task.get('task_name', 'Unknown Task')}\n\n")
        
        file.write(f"**Status:** {'✅ Completed' if task.get('completed', False) else '❌ Failed'}\n\n")
        file.write(f"**Prompt:**\n")
        file.write(f"{task.get('prompt', 'N/A')}\n\n")
        
        # Find corresponding API call
        if i < len(api_calls_history):
            api_call = api_calls_history[i]
            _write_api_call_details(file, api_call, task_num)
        
        # Write response
        response = task.get('response')
        if response:
            file.write(f"**AI Response:**\n\n")
            file.write(f"{response}\n\n")
        else:
            file.write(f"**AI Response:** No response received\n\n")
        
        file.write("---\n\n")


def _write_interactive_session(file, interactions: List[Dict[str, Any]], api_calls_history: List[Dict[str, Any]]):
    """Helper function to write interactive session section."""
    for i, interaction in enumerate(interactions):
        file.write(f"### Interaction {i + 1} - {interaction.get('timestamp', 'N/A')}\n\n")
        
        file.write(f"**Context:** {interaction.get('context_description', 'N/A')} ({interaction.get('context_size', 0)} characters)\n\n")
        file.write(f"**Status:** {'✅ Success' if interaction.get('success', False) else '❌ Failed'}\n\n")
        
        file.write(f"**👤 User Question:**\n")
        file.write(f"{interaction.get('user_question', 'N/A')}\n\n")
        
        # Find corresponding API call
        if i < len(api_calls_history):
            api_call = api_calls_history[i]
            _write_api_call_details(file, api_call, i + 1)
        
        # Write response
        response = interaction.get('assistant_response')
        if response:
            file.write(f"**🤖 Assistant Response:**\n\n")
            file.write(f"{response}\n\n")
        else:
            file.write(f"**🤖 Assistant Response:** No response received\n\n")
        
        file.write("---\n\n")


def _write_custom_context_analysis(file, tasks: List[Dict[str, Any]], api_calls_history: List[Dict[str, Any]]):
    """Helper function to write custom context analysis section."""
    if tasks:
        task = tasks[0]  # Should only be one task for custom context
        file.write(f"### {task.get('task_name', 'Custom Analysis')}\n\n")
        
        file.write(f"**Status:** {'✅ Completed' if task.get('completed', False) else '❌ Failed'}\n\n")
        
        # Show the user's custom code if available
        if 'code_content' in task:
            file.write(f"**User's Code:**\n\n")
            file.write("```\n")
            file.write(task['code_content'])
            file.write("\n```\n\n")
        
        file.write(f"**Analysis Prompt:**\n")
        file.write(f"{task.get('prompt', 'N/A')}\n\n")
        
        # Write API call details
        if api_calls_history:
            api_call = api_calls_history[0]
            _write_api_call_details(file, api_call, 1)
        
        # Write response
        response = task.get('response')
        if response:
            file.write(f"**AI Analysis:**\n\n")
            file.write(f"{response}\n\n")
        else:
            file.write(f"**AI Analysis:** No response received\n\n")


def _write_api_call_details(file, api_call: Dict[str, Any], call_number: int):
    """Helper function to write API call details."""
    file.write(f"#### 🔄 API Request #{call_number}\n\n")
    file.write(f"- **Endpoint:** `{api_call.get('url', 'N/A')}`\n")
    file.write(f"- **Method:** `POST`\n")
    file.write(f"- **Status Code:** `{api_call.get('status_code', 'N/A')}`\n")
    file.write(f"- **Response Time:** `{api_call.get('response_time', 'N/A')}ms`\n")
    file.write(f"- **Context Size:** `{api_call.get('context_size', 'N/A')} characters`\n")
    file.write(f"- **Context Description:** {api_call.get('context_description', 'N/A')}\n\n")
    
    # Show headers (redacted)
    if 'headers' in api_call:
        file.write("**Request Headers:**\n")
        for header, value in api_call['headers'].items():
            if 'token' in header.lower() or 'authorization' in header.lower():
                value = '[REDACTED]'
            file.write(f"- `{header}: {value}`\n")
        file.write("\n")
    
    # Show request payload
    if 'request_payload' in api_call:
        file.write("**Request Payload:**\n\n")
        file.write("```json\n")
        import json
        file.write(json.dumps(api_call['request_payload'], indent=2, ensure_ascii=False))
        file.write("\n```\n\n")
    
    # Show token usage
    usage = api_call.get('usage', {})
    if usage:
        file.write("**Token Usage:**\n")
        file.write(f"- Prompt Tokens: `{usage.get('prompt_tokens', 'N/A')}`\n")
        file.write(f"- Completion Tokens: `{usage.get('completion_tokens', 'N/A')}`\n")
        file.write(f"- Total Tokens: `{usage.get('total_tokens', 'N/A')}`\n\n")
    
    # Show errors if any
    if 'error' in api_call:
        error = api_call['error']
        file.write("**⚠️ Error Details:**\n")
        file.write(f"- **Type:** `{error.get('type', 'N/A')}`\n")
        file.write(f"- **Message:** {error.get('message', 'N/A')}\n")
        if 'status_code' in error:
            file.write(f"- **Status Code:** `{error.get('status_code', 'N/A')}`\n")
        if 'response_body' in error:
            file.write(f"- **Response Body:** {error.get('response_body', 'N/A')[:200]}...\n")
        file.write("\n")
