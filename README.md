# Sourcegraph Cody API Cookbook 🍳

A comprehensive collection of Python examples demonstrating how to use the Sourcegraph Cody API. Each script focuses on a specific aspect of the API, from basic authentication to advanced features like tool calling and context search. This cookbook serves as both a learning resource and a practical reference for developers building AI-powered applications with Sourcegraph Cody.

## 🎯 What This Cookbook Covers

- **API Authentication & Basic Operations** - Models, authentication, and basic chat
- **Advanced AI Capabilities** - Tool/function calling, context search, and manual context passing
- **Practical Code Examples** - Real-world use cases with comprehensive error handling
- **Educational Features** - Verbose output, usage statistics, and response file saving
- **Production Patterns** - Best practices for authentication, error handling, and token management

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- A Sourcegraph account with API access
- Access token from your Sourcegraph instance

### Installation

1. **Clone or download this cookbook**
   ```bash
   cd cody-cookbook
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Copy the example environment file and fill in your values:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your actual values:
   ```bash
   SOURCEGRAPH_URL=https://sourcegraph.com
   SOURCEGRAPH_ACCESS_TOKEN=your_access_token_here
   SOURCEGRAPH_X_REQUESTED_WITH=cody-cookbook
   ```

   Replace:
   - `https://sourcegraph.com` with your Sourcegraph instance URL
   - `your_access_token_here` with your actual access token
   - `cody-cookbook` with your application name (optional, defaults to 'cody-cookbook')

## 📚 Examples

### 00-models.py - List Available Models
Lists all available LLM models from your Sourcegraph instance.

```bash
python 00-models.py
```

**What you'll learn:**
- How to authenticate with the API
- Basic GET request structure
- Understanding model IDs and their format

### 01-modelinstance.py - Get Model Details
Retrieves detailed information about a specific model.

```bash
python 01-modelinstance.py anthropic::2024-10-22::claude-sonnet-4-latest
```

**What you'll learn:**
- Working with path parameters
- Error handling for invalid model IDs
- Model metadata structure

### 02-chat.py - Chat Completions
Interactive chat with AI models, demonstrating temperature and token controls.

```bash
python 02-chat.py [model_id]
```

**What you'll learn:**
- POST requests with JSON payloads
- Interactive user input handling
- Temperature and max_tokens parameters
- Usage statistics and token counting

**Features:**
- Interactive chat mode
- Adjustable temperature (0.0-1.0)
- Configurable max tokens (1-4000)
- Usage statistics display

### 03-tools.py - Function/Tool Calling
Demonstrates the complete tool calling workflow, showing how AI models can execute functions to perform specific tasks. This script provides full API transparency, displaying every request and response in the tool calling conversation.

```bash
python 03-tools.py [model_id]
```

**What you'll learn:**
- **Complete Tool Calling Workflow**: Step-by-step process from initial request to final response
- **Function Definition**: How to structure tool schemas with proper JSON Schema validation
- **API Request/Response Flow**: Full visibility into the JSON payloads exchanged with the API
- **Multi-turn Conversations**: How the AI decides which tools to use and when
- **Error Handling**: Robust handling of tool execution failures and API errors

**🔧 How Tool Calling Works:**

Tool calling (also known as function calling) is a powerful feature that allows AI models to interact with external systems and APIs. Here's the complete workflow:

1. **Tool Definition Phase**:
   - Define available functions with JSON Schema specifications
   - Include function names, descriptions, and parameter definitions
   - Send these definitions in the `tools` array of your API request

2. **AI Decision Phase**:
   - The AI analyzes the user's request and available tools
   - Determines which tool(s) to use based on the request context
   - Returns a `tool_use` response with function calls instead of text

3. **Function Execution Phase**:
   - Your application extracts tool calls from the AI response
   - Executes the actual functions with provided parameters
   - Collects the results from each function execution

4. **Result Integration Phase**:
   - Send function results back to the AI in a new message
   - AI processes the results and generates a final human-readable response
   - The conversation continues naturally with the function outputs integrated

**Available Example Tools:**
- **Weather Lookup** (simulated): Demonstrates external API simulation
- **Mathematical Calculations**: Shows parameter validation and computation
- **Current Time/Date**: Simple function with no parameters

**🎨 Key Features:**
- **Full API Transparency**: See every JSON request and response
- **Interactive Mode**: Ask questions that trigger different tool combinations
- **Conversation Memory**: Multi-turn conversations with tool state persistence
- **Error Recovery**: Graceful handling of tool failures and retries

### 04-context.py - Code Context Search
Leverages Sourcegraph's powerful code search capabilities to find relevant code examples from repositories using natural language queries. This demonstrates how Cody's context search API can understand semantic code relationships and retrieve relevant snippets.

```bash
python 04-context.py
```

**What you'll learn:**
- **Natural Language Code Search**: Query code using human-readable descriptions
- **Repository Specification**: Target specific repositories for focused searches
- **Advanced File Filtering**: Use regex patterns to narrow search scope
- **Context Processing**: Handle and display search results with code snippets
- **Search Strategy Optimization**: Understand how different query patterns affect results

**🔍 How Cody Context Search Works:**

Sourcegraph's context search combines traditional code search with semantic understanding:

1. **Query Processing**: Natural language queries are processed to understand intent
2. **Repository Indexing**: Sourcegraph maintains indexes of code structure and relationships
3. **Semantic Matching**: The system finds code that matches not just keywords but concepts
4. **Ranking & Relevance**: Results are ranked by relevance to the query and code quality
5. **Snippet Extraction**: Relevant code snippets are extracted with surrounding context

**🎨 Features:**
- **Three Search Modes**:
  - **Examples Mode**: Pre-built queries demonstrating different search patterns
  - **Interactive Search**: Custom queries with immediate results
  - **Conversational Search**: Multi-turn conversations building on previous searches
- **Search History Tracking**: Remember and reference previous searches
- **Configurable Result Counts**: Control the number of results returned
- **Regex File Pattern Filtering**: Target specific file types (e.g., `\.go$`, `.*test.*`)
- **Multiple Repository Search**: Search across multiple repositories simultaneously
- **Rich Output Formatting**: Code syntax highlighting and structured result display

### 05-manual-context.py - Manual Context Passing
Demonstrates advanced manual context passing techniques for precise code analysis and refactoring. This script shows how to provide specific code context directly to the AI for targeted analysis, bypassing automatic context retrieval when you need full control over what the AI sees.

```bash
python 05-manual-context.py [model_id]
```

**What you'll learn:**
- **Strategic Context Management**: When and why to use manual vs. automatic context
- **Context Structuring**: Optimal ways to format code context for AI analysis
- **Prompt Engineering**: Crafting effective prompts for different analysis types
- **Multi-modal Analysis**: Security, performance, and code quality assessments
- **Response Processing**: Handling and saving detailed AI analysis results

**🧠 Why Manual Context Passing Matters:**

While automatic context retrieval (like in `04-context.py`) is powerful, manual context passing offers several advantages:

1. **Precision Control**: Provide exactly the code that needs analysis without noise
2. **Security Sensitivity**: Control what code is sent to AI models for privacy/security
3. **Context Size Management**: Optimize token usage by including only relevant code
4. **Custom Analysis Types**: Structure context specifically for the type of analysis needed
5. **Offline Analysis**: Analyze code without requiring repository indexing or search

**🎯 Use Cases for Manual Context:**

- **Security Audits**: Focus on specific functions or modules with known vulnerabilities
- **Legacy Code Refactoring**: Analyze old code that may not be well-indexed
- **Code Review Preparation**: Pre-analyze code before human code reviews
- **Bug Investigation**: Provide specific problematic code sections for debugging
- **Performance Optimization**: Target specific performance-critical code paths

**🎨 Features:**
- **Multiple Analysis Modes**:
  - **Refactoring Examples**: Pre-configured analysis tasks (security, performance, quality)
  - **Interactive Mode**: Custom context with real-time analysis
  - **Custom Context Creator**: Template-driven analysis for specific scenarios
- **Flexible Input Methods**:
  - Load context from files
  - Paste code directly
  - Use provided sample code with intentional issues
- **Response Management**:
  - **Automatic File Saving**: All responses saved to timestamped files
  - **Organized Output**: Responses saved in `responses/` directory with descriptive names
  - **Rich Formatting**: Markdown-formatted responses with metadata headers
- **Analysis Templates**:
  - Security vulnerability assessment
  - Performance bottleneck identification
  - Code quality improvement suggestions
  - Bug identification and fixes
  - Best practices recommendations

**📁 Response File Management:**

All AI responses are automatically saved to timestamped files in the `responses/` directory:
- **Format**: `YYYYMMDD_HHMMSS_task_name.md`
- **Content**: Full AI response with metadata header
- **Organization**: Easy to find and reference later for documentation or follow-up

## 🛠️ API Endpoints Covered

| Script | Endpoint | Method | Description |
|--------|----------|--------|-------------|
| 00-models.py | `/.api/llm/models` | GET | List available models |
| 01-modelinstance.py | `/.api/llm/models/{modelId}` | GET | Get model details |
| 02-chat.py | `/.api/llm/chat/completions` | POST | Chat completions |
| 03-tools.py | `/.api/llm/chat/completions` | POST | Chat with function calling |
| 04-context.py | `/.api/cody/context` | POST | Code context search |
| 05-manual-context.py | `/.api/llm/chat/completions` | POST | Chat with manual context |

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Required
SOURCEGRAPH_URL=https://your-instance.sourcegraph.com
SOURCEGRAPH_ACCESS_TOKEN=sgp_your_token_here
SOURCEGRAPH_X_REQUESTED_WITH=cody-cookbook

# Optional - these are defaults used in scripts
DEFAULT_MODEL=anthropic::2024-10-22::claude-sonnet-4-latest
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=4000
```

### Authentication

The API uses token-based authentication and requires a custom header. Include both in requests:

```bash
Authorization: token YOUR_ACCESS_TOKEN
X-Requested-With: YOUR_APP_NAME
```

### Model ID Format

Model IDs follow the pattern: `${ProviderID}::${APIVersionID}::${ModelID}`

Examples:
- `anthropic::2024-10-22::claude-sonnet-4-latest`
- `anthropic::2023-06-01::claude-3.5-sonnet`
- `openai::2024-02-01::gpt-4o`
- `mistral::v1::mixtral-8x7b-instruct`

## 📋 Project Structure

```
cody-cookbook/
├── 00-models.py              # List available models
├── 01-modelinstance.py       # Get model details  
├── 02-chat.py               # Interactive chat with conversation memory
├── 03-tools.py              # Function/tool calling with full API transparency
├── 04-context.py            # Code context search with multiple modes
├── 05-manual-context.py     # Manual context passing with file saving
├── requirements.txt         # Python dependencies
├── .env.example            # Environment configuration template
├── sample-code.md          # Intentionally flawed code for refactoring examples
└── responses/              # Auto-generated directory for AI responses
```

## 🎯 Usage Tips & Best Practices

### Getting Started
1. **Start with 00-models.py** to see what models are available in your instance
2. **Test connectivity** with a simple model query (01-modelinstance.py) before complex operations
3. **Copy .env.example to .env** and configure your credentials properly

### API Optimization
4. **Monitor token usage** to understand costs and limits (visible in all scripts)
5. **Use appropriate temperatures** (lower 0.1-0.3 for factual, higher 0.7-1.0 for creative)
6. **Set reasonable max_tokens** to control response length and costs
7. **Leverage conversation memory** in interactive scripts for context continuity

### Tool Calling Best Practices
8. **Start simple** with 03-tools.py to understand the request/response flow
9. **Design functions with clear descriptions** for better AI decision-making
10. **Validate function parameters** before execution to prevent errors
11. **Handle tool failures gracefully** with try-catch blocks and fallback responses

### Context Management
12. **Use 04-context.py for discovery** when you need to find relevant code
13. **Use 05-manual-context.py for precision** when you know exactly what to analyze
14. **Save important responses** using the automatic file saving feature
15. **Structure context appropriately** for the type of analysis you need

## 🚨 Common Issues

### Authentication Errors
- Verify your access token is correct
- Check that your Sourcegraph URL is correct
- Ensure your token has the necessary permissions

### Model Not Found
- Run `00-models.py` to see available models
- Check the model ID format is correct
- Some models may not be available in your instance

### Rate Limiting
- Add delays between requests if you hit rate limits
- Monitor your usage statistics

## 💡 Advanced Topics & Deep Dives

### Understanding Tool Calling Architecture

Tool calling represents a paradigm shift in AI interaction, moving from passive Q&A to active task execution. This cookbook's `03-tools.py` demonstrates the complete workflow:

- **Declarative Function Definition**: Functions are described using JSON Schema, not executed code
- **AI Decision Engine**: The model analyzes user intent and selects appropriate tools
- **Execution Boundary**: Your application controls the actual function execution, maintaining security
- **Result Integration**: Function outputs are seamlessly integrated into natural language responses

### Context Strategy: Automatic vs Manual

The choice between automatic context search (`04-context.py`) and manual context passing (`05-manual-context.py`) depends on your use case:

**Use Automatic Context When:**
- Exploring unfamiliar codebases
- Need to find examples across multiple repositories  
- Want to discover related code patterns
- Building general-purpose coding assistants

**Use Manual Context When:**
- Analyzing specific, known problematic code
- Security-sensitive analysis requiring controlled input
- Working with legacy or poorly-indexed code
- Need precise control over token usage and costs

### Response File Management System

The automatic response saving in `05-manual-context.py` implements a production-ready pattern:
- **Timestamped Organization**: Easy to track analysis history
- **Metadata Preservation**: Context and task information included
- **Markdown Format**: Human-readable and tool-processable
- **Scalable Structure**: Organized directory structure for large-scale usage

## 🔗 Additional Resources & References

### AI & Tool Calling References
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) - Official Claude tool calling guide
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) - OpenAI's approach to function calling


### Community & Support
- [Sourcegraph Community Forum](https://community.sourcegraph.com/) - Ask questions and share solutions
- [Cody Discord Community](https://discord.gg/sourcegraph) - Real-time community support
- [GitHub Issues](https://github.com/sourcegraph/cody/issues) - Report bugs and request features

## 📝 License

This cookbook is provided as educational examples. Check your Sourcegraph license for API usage terms.

---

Happy coding! 🎉 If you have questions or suggestions, feel free to reach out or contribute improvements to these examples.
