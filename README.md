# Simple MCP-server to make pdf based on IA interaction

This repository it's a simple implementation of mcp-server to create pdfs using IA agents.

## Json to run mcpServer

Import this json in your configuracion of mcp-servers to use it.

```json
{

  "mcpServers": {
    "server": {
      "command": "<python environment with fastmcp binary> (ej.~/envs/pdf-mcp/bin/fastmcp)",
      "args": [
        "run",
        "<path of main.py of this repository> (ej. ~/pdf-mcp/main.py:mcp)"
      ],
      "env": {
        "PDF_OUTPUT_DIR": "<output folder path where pdf will be sent>",
        "PDF_STYLESHEET_PATH": "<path of styles.css, you can use your css styles or use the css file of this repository> (ej. ~/mcp_server/styles/styles.css)",
        "PDF_HEADER_PATH": "<Path with the header image > (ej. ~/header.png)"
      }
    }
  }
}
```

> Remember that each path should be the absolute path

## Transport

At the moment, this mcp-server works in `stdio` transport.
