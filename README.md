# Prisma Cloud Docs MCP Server

[![smithery badge](https://smithery.ai/badge/@clarkemn/prisma-cloud-docs-mcp-server)](https://smithery.ai/server/@clarkemn/prisma-cloud-docs-mcp-server)

<a href="https://glama.ai/mcp/servers/@clarkemn/prisma-cloud-docs-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@clarkemn/prisma-cloud-docs-mcp-server/badge" />
</a>

A Model Context Protocol (MCP) server that provides search access to Prisma Cloud documentation. This server allows Claude and other MCP-compatible clients to search through Prisma Cloud's official documentation and API references.

> **Note:** This server has been migrated to HTTP transport and container deployment for improved scalability and performance. The server now runs in HTTP mode when deployed via Smithery.

## Features

- Search across Prisma Cloud documentation
- Search Prisma Cloud API documentation  
- Caching system for improved performance
- Real-time indexing of documentation sites

## Installation

### Option 1: From PyPI (Recommended)

No installation needed! Just use `uvx` in your Claude Desktop configuration.

### Installing via Smithery

To install prisma-cloud-docs-mcp-server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@clarkemn/prisma-cloud-docs-mcp-server):

```bash
npx -y @smithery/cli install @clarkemn/prisma-cloud-docs-mcp-server --client claude
```

### Option 2: Development Installation

#### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

#### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Clone and Setup

```bash
git clone https://github.com/clarkemn/prisma-cloud-docs-mcp-server.git
cd prisma-cloud-docs-mcp-server
uv sync
```

## Usage

### With Claude Desktop

Add this server to your Claude Desktop configuration file:

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

#### Option 1: Direct from PyPI (Recommended)

```json
{
  "mcpServers": {
    "Prisma Cloud Docs": {
      "command": "uvx",
      "args": ["prisma-cloud-docs-mcp-server@latest"],
      "env": {},
      "transport": "stdio"
    }
  }
}
```

#### Option 2: Local Development

```json
{
  "mcpServers": {
    "Prisma Cloud Docs": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/prisma-cloud-docs-mcp-server",
      "env": {},
      "transport": "stdio"
    }
  }
}
```

Replace `/path/to/prisma-cloud-docs-mcp-server` with the actual path to where you cloned this repository.

### Manual Testing

You can test the server manually:

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}' | uv run python server.py
```

## Available Tools

The server provides these MCP tools:

- `index_prisma_docs(max_pages: int = 50)` - Index Prisma Cloud documentation (call this first)
- `index_prisma_api_docs(max_pages: int = 50)` - Index Prisma Cloud API documentation  
- `search_prisma_docs(query: str)` - Search Prisma Cloud documentation
- `search_prisma_api_docs(query: str)` - Search Prisma Cloud API documentation
- `search_all_docs(query: str)` - Search across all indexed documentation
- `get_index_status()` - Check indexing status and cache statistics

## Development

### Running the server

#### HTTP mode (Production/Smithery):
```bash
uv run python -m src.main
```

#### STDIO mode (Local development):
```bash
uv run python server.py
```

#### Container mode:
```bash
docker build -t prisma-docs-server .
docker run -p 8081:8081 -e PORT=8081 prisma-docs-server
```

### Installing dependencies

```bash
uv sync
```

### Project structure

```
prisma-cloud-docs-mcp-server/
├── src/
│   ├── main.py           # HTTP MCP server implementation  
│   └── middleware.py     # Configuration middleware for Smithery
├── server.py             # Legacy STDIO server (for local development)
├── pyproject.toml        # Project configuration
├── uv.lock              # Dependency lock file
├── Dockerfile           # Container deployment
├── smithery.yaml        # Smithery container configuration
└── README.md            # This file
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Claude Desktop
5. Submit a pull request

## Troubleshooting

### Server not starting in Claude Desktop

1. Ensure `uv` is installed and in your PATH
2. Verify the path to the project directory is correct
3. Check Claude Desktop logs for specific error messages

### Missing dependencies

Run `uv sync` to ensure all dependencies are installed.

### Documentation not found

The server needs to index documentation first. Use the `index_prisma_docs` or `index_prisma_api_docs` tools before searching.
