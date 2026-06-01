# MCP Python Setup - Learning Project

A learning project to understand **Model Context Protocol (MCP)** in Python, demonstrating integration between MCP Server, MCP Client, and Claude AI.

## 📁 Project Structure

```
py_setup_mcp/
├── main.py                 # Entry point - orchestrates MCP clients & Claude
├── mcp_server.py          # MCP Server using FastMCP (Document Management)
├── mcp_client.py          # MCP Client for communicating with server
├── pyproject.toml         # Project configuration & dependencies
├── .env                   # Environment variables (CLAUDE_MODEL, ANTHROPIC_API_KEY)
│
├── core/
│   ├── __init__.py
│   ├── claude.py          # Claude AI service wrapper
│   ├── chat.py            # Chat logic
│   ├── cli_chat.py        # CLI chat interface
│   ├── cli.py             # CLI application framework
│   └── tools.py           # Tool utilities
│
└── local_llm/
    ├── agent.py           # Local agent implementation
    └── weather_server.py  # Example: Weather MCP Server
```

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10+
- API Key from Anthropic (Claude)
- `uv` package manager (optional, for development)

### 2. Clone & Install Dependencies

```bash
# Navigate to project directory
cd py_setup_mcp

# Install dependencies using uv
uv sync

# Or using pip
pip install -e .
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```bash
# .env
CLAUDE_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=your-api-key-here
USE_UV=1  # Set to 1 if using uv, 0 for python
```

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | ≥0.51.0 | Claude API client |
| `mcp` | ≥1.8.0 | Model Context Protocol SDK |
| `prompt-toolkit` | ≥3.0.51 | Interactive CLI interface |
| `python-dotenv` | ≥1.1.0 | Environment variables management |

## 🔧 Core Components

### 1. MCP Server (`mcp_server.py`)

FastMCP server that provides tools for document management:

**Available Tools:**
- `read_doc_contents` - Read document contents by ID
- `edit_document` - Edit document content

**Stored Documents:**
- `deposition.md` - Testimony documentation
- `report.pdf` - Technical report
- `financials.docx` - Budget & expenditure
- `outlook.pdf` - Performance projection
- `plan.md` - Implementation plan
- `spec.txt` - Technical specifications

### 2. MCP Client (`mcp_client.py`)

Asynchronous MCP client that:
- Creates stdio connection to MCP Server
- Manages session and resources
- Handles tool calls and responses

### 3. Claude Service (`core/claude.py`)

Wrapper for Anthropic API that:
- Manages conversation history
- Adds/reads messages
- Extracts text from responses

### 4. Main Orchestrator (`main.py`)

Main coordinator that:
- Initializes Claude service
- Creates multiple MCP clients
- Manages async context management
- Connects all components

## 🎮 Usage Guide

### Run Main Application

```bash
# Using uv
uv run main.py

# Or using python
python main.py
```

### Run with External Server

```bash
# Run main with external server script
uv run main.py local_llm/weather_server.py
```

### Interactive Chat

The application opens an interactive chat interface in CLI where you can:
- Ask questions to Claude
- Claude will use available tools from MCP servers
- Iterate through the conversation

## 🛠️ Development Tips

### Debug Mode
Edit `mcp_server.py` to change log level:
```python
mcp = FastMCP("DocumentMCP", log_level="DEBUG")  # Change ERROR to DEBUG
```

### Test Tools Manually
```python
# Test in Python REPL
from mcp_server import read_document
print(read_document("deposition.md"))
```

### Async Testing
```bash
# Install pytest-asyncio for async code testing
uv pip install pytest-asyncio
```

## 📚 Important Concepts

### Model Context Protocol
MCP is a standard protocol for:
- Connecting LLMs to external tools & data
- Providing structured access to resources
- Enabling sophisticated AI applications

### AsyncIO Pattern
This project uses `AsyncExitStack` to:
- Manage multiple async resources
- Automatic cleanup on exit
- Robust error handling

### Tool-Calling Loop
Claude can:
1. Receive tool definitions from MCP server
2. Call tools based on user query
3. Use results to generate response

## 🎓 Learning Resources

To deepen your understanding:
- [MCP Documentation](https://modelcontextprotocol.io)
- [Anthropic Claude API](https://docs.anthropic.com)
- [FastMCP Guide](https://mcp.anthropic.com)
- [Python AsyncIO](https://docs.python.org/3/library/asyncio.html)

## ⚙️ Environment Variables Reference

```bash
# Required
ANTHROPIC_API_KEY=your-api-key

# Optional
CLAUDE_MODEL=claude-3-5-sonnet-20241022  # Default model
USE_UV=0                                  # Use uv package manager (1=yes, 0=no)
```

**Happy Learning! 🚀**

If you have questions or want to discuss MCP, open an issue or check the documentation links above.
