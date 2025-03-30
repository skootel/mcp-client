"""
Main entry point for the van dispatcher agent.
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from van_dispatcher import graph
from langserve import add_routes

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

app = FastAPI(title="Van Dispatcher Agent")
add_routes(app, graph, path="/agent")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
