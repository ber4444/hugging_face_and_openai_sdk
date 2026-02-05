import asyncio
from agents import Agent, Runner, set_default_openai_key
from openai.types.responses import ResponseTextDeltaEvent
from agents.mcp.server import MCPServerStreamableHttp
from agents.model_settings import ModelSettings

import os

set_default_openai_key(os.getenv("OPENAI_API_KEY"))

async def main():
    async with MCPServerStreamableHttp(
        name="DeepWiki MCP Server",
        params={
            "url": "https://mcp.deepwiki.com/mcp",
        },
        client_session_timeout_seconds=30
    ) as mcp_server:
        agent = Agent(
            name="DeepWiki Agent",
            instructions="Use the tools to answer the questions.",
            mcp_servers=[mcp_server],
        )

        prompt = """Take a look at deepwiki and figure out What transport
                    protocols are supported in the 2025-03-26 version of the MCP spec?
                    Using the modelcontextprotocol/python-sdk repo"""


        response = Runner.run_streamed(agent, prompt)
        async for event in response.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

asyncio.run(main())
