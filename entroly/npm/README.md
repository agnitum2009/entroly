# entroly-mcp

NPM bridge for the Entroly MCP server. This package wraps the Python `entroly` CLI so you can use it with Cursor, VS Code, and other MCP clients that prefer npm-based tool installation.

## Prerequisites

You need the Python `entroly` package installed:

```bash
pip install entroly
```

## Usage with Cursor

Add to your Cursor MCP config (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "entroly": {
      "command": "npx",
      "args": ["-y", "entroly-mcp"]
    }
  }
}
```

## What this does

This is a **thin bridge** — it simply calls `entroly serve` under the hood. All the actual context optimization runs in the Entroly Python package backed by the `entroly-core` Rust engine.

For more info, see the [main repo](https://github.com/juyterman1000/entroly).
