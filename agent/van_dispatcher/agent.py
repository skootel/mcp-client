"""
Van Dispatcher Agent using MCP servers.
This agent connects to Slack, Browserbase, Memory, and SequentialThinking MCP servers
to manage van status and dispatch operations.
"""

from typing_extensions import Literal, TypedDict, Dict, List, Any, Union, Optional
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from copilotkit import CopilotKitState
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from copilotkit.langgraph import (copilotkit_exit)
import os
import json
from datetime import datetime
from pydantic import BaseModel, Field

class StdioConnection(TypedDict, total=False):
    command: str
    args: List[str]
    transport: Literal["stdio"]
    env: Dict[str, str]

class SSEConnection(TypedDict):
    url: str
    transport: Literal["sse"]

MCPConfig = Dict[str, Union[StdioConnection, SSEConnection]]

class AgentState(CopilotKitState):
    """
    State for the van dispatcher agent.
    """
    mcp_config: Optional[MCPConfig]

class Van(BaseModel):
    """Model for van information."""
    id: str = Field(description="Unique identifier for the van")
    name: str = Field(description="Human-readable name for the van")
    status: str = Field(description="Current operational status (available, not-available)")
    slack_channel_id: str = Field(description="Dedicated Slack channel for van communications")
    capacity: int = Field(description="Maximum number of scooters the van can transport")
    region: str = Field(description="Geographical region where the van operates (metro, west)")

class VanDispatcherOutput(BaseModel):
    """Output model for the van dispatcher agent."""
    van: Van = Field(description="Single van with its updated status")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp of when the van status was updated")
    success: bool = Field(description="Whether the update was successful")
    message: str = Field(description="Status message about the update")

class SlackVanStatus(BaseModel):
    """Model for van status information retrieved from Slack."""
    id: str
    name: str
    status: str
    last_updated: str
    channel_id: str
    notes: str

class SlackVanStatusOutput(BaseModel):
    """Output model for the Slack agent with van status information."""
    vans: List[SlackVanStatus] = Field(default_factory=list, description="List of vans with their status from Slack")

def read_prompt_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

PROMPT_BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "prompts", "van")
SLACK_AGENT_PROMPT_PATH = os.path.join(PROMPT_BASE_PATH, "slack_agent_prompt.md")
VAN_DISPATCHER_PROMPT_PATH = os.path.join(PROMPT_BASE_PATH, "dispatcher_prompt.md")
GUARDRAIL_PROMPT_PATH = os.path.join(PROMPT_BASE_PATH, "guardrail_prompt.md")

VAN_INFO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "knowledge", "van", "van_info.md")

slack_agent_prompt = read_prompt_from_file(SLACK_AGENT_PROMPT_PATH)
van_dispatcher_prompt = read_prompt_from_file(VAN_DISPATCHER_PROMPT_PATH)
guardrail_prompt = read_prompt_from_file(GUARDRAIL_PROMPT_PATH)
van_info = read_prompt_from_file(VAN_INFO_PATH)

DEFAULT_MCP_CONFIG: MCPConfig = {
    "slack": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
        "transport": "stdio",
        "env": {
            "SLACK_BOT_TOKEN": os.environ.get("SLACK_BOT_TOKEN", ""),
            "SLACK_TEAM_ID": os.environ.get("SLACK_TEAM_ID", "")
        }
    },
    "browserbase": {
        "command": "npx",
        "args": ["-y", "@browserbase/mcp-server-browserbase"],
        "transport": "stdio",
        "env": {
            "BROWSERBASE_API_KEY": os.environ.get("BROWSERBASE_API_KEY", "")
        }
    },
    "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "transport": "stdio"
    },
    "sequentialthinking": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sequentialthinking"],
        "transport": "stdio"
    }
}

async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["__end__"]]:
    """
    Main chat node for the van dispatcher agent.
    """
    mcp_config = state.get("mcp_config", DEFAULT_MCP_CONFIG)
    
    print(f"Using MCP configuration: {mcp_config}")
    
    async with MultiServerMCPClient(mcp_config) as mcp_client:
        mcp_tools = mcp_client.get_tools()
        
        model = ChatOpenAI(model="gpt-4o")
        
        combined_prompt = f"{van_dispatcher_prompt}\n\n## Additional Van Information\n\n{van_info}"
        
        system_message = {"role": "system", "content": combined_prompt}
        
        messages = state.get("messages", [])
        if messages and messages[0].get("role") != "system":
            messages = [system_message] + messages
        elif not messages:
            messages = [system_message]
        
        react_agent = create_react_agent(model, mcp_tools)
        
        agent_input = {
            "messages": messages
        }
        
        agent_response = await react_agent.ainvoke(agent_input)
        
        updated_messages = state["messages"] + agent_response.get("messages", []) 
        
        try:
            for message in agent_response.get("messages", []):
                if message.get("role") == "assistant" and message.get("content"):
                    content = message.get("content")
                    import re
                    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1)
                        try:
                            van_data = json.loads(json_str)
                            latest_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                                    "knowledge", "van", "latest_van_status.json")
                            with open(latest_path, "w") as f:
                                json.dump(van_data, f, indent=2)
                            print(f"Saved van status to {latest_path}")
                        except json.JSONDecodeError:
                            print(f"Failed to parse JSON from content: {json_str}")
        except Exception as e:
            print(f"Error saving van status: {e}")
        
        await copilotkit_exit(config)
        return Command(
            goto=END,
            update={"messages": updated_messages},
        )

workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.set_entry_point("chat_node")

graph = workflow.compile(MemorySaver())
