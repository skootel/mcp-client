"""
Main entry point for the van dispatcher agent.
"""
import os
import sys
from dotenv import load_dotenv
from van_dispatcher import graph
from copilotkit.langgraph import run_copilotkit_server

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

if __name__ == "__main__":
    run_copilotkit_server(graph, port=3001)
