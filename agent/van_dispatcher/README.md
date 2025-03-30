# Van Dispatcher Agent

This agent connects to Slack, Browserbase, Memory, and SequentialThinking MCP servers to manage van status and dispatch operations.

## Overview

The Van Dispatcher Agent is designed to:
1. Connect to multiple MCP servers (Slack, Browserbase, Memory, SequentialThinking)
2. Check van status through Slack channels
3. Update van status information in the knowledge base
4. Provide a chat interface for van dispatch operations

## Setup Instructions

### 1. Environment Variables

Create or update the `.env` files with the necessary API keys and tokens:

**Root `.env` file:**
```
# MCP Client Environment Variables
OPENAI_API_KEY=sk-your-openai-api-key
LANGSMITH_API_KEY=lsv2-your-langsmith-api-key

# Slack MCP Server Environment Variables
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_TEAM_ID=your-slack-team-id

# Browserbase MCP Server Environment Variables
BROWSERBASE_API_KEY=your-browserbase-api-key
```

**Agent `.env` file:**
```
# Agent Environment Variables
OPENAI_API_KEY=sk-your-openai-api-key
LANGSMITH_API_KEY=lsv2-your-langsmith-api-key

# Slack MCP Server Environment Variables
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_TEAM_ID=your-slack-team-id

# Browserbase MCP Server Environment Variables
BROWSERBASE_API_KEY=your-browserbase-api-key
```

### 2. Install Dependencies

```bash
# Install frontend dependencies
cd ~/repos/mcp-client
pnpm install

# Install agent dependencies
cd agent
poetry install
```

## Testing Instructions

### 1. Start the MCP Client

Run the frontend and agent in separate terminals:

```bash
# Terminal 1 - Frontend
cd ~/repos/mcp-client
pnpm run dev-frontend

# Terminal 2 - Agent
cd ~/repos/mcp-client/agent
poetry run python main.py
```

### 2. Test Van Dispatcher Agent

1. Open the MCP Client interface in your browser
2. Start a new chat session
3. Ask about van status, for example:
   - "What is the status of van-1?"
   - "Are there any available vans in the metro region?"
   - "Check the status of all vans"

### 3. Verify Van Status Updates

The agent will:
1. Connect to the Slack MCP server
2. Check the specified Slack channel for van status
3. Update the van status in the knowledge base
4. Return the updated status information

You can verify the updates by checking the `knowledge/van/latest_van_status.json` file.

### 4. Test with Sample Van Data

The repository includes sample van data in `knowledge/van/fleet/van-1.json`. You can add more van data files to test with multiple vans.

## Troubleshooting

### Common Issues

1. **MCP Server Connection Errors**:
   - Verify that the environment variables are set correctly
   - Check that the MCP servers are installed and accessible

2. **Slack API Errors**:
   - Ensure the Slack bot token has the necessary permissions
   - Verify that the Slack team ID is correct

3. **Agent Not Responding**:
   - Check the agent logs for any errors
   - Verify that the OpenAI API key is valid

### Logs

The agent logs are printed to the console. Check the agent terminal for any error messages or debugging information.
