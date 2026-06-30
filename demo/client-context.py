import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from mcp.types import LoggingMessageNotificationParams
import os
import dotenv

dotenv.load_dotenv()

class LoggingCollector:
    def __init__(self):
        self.log_messages: list[LoggingMessageNotificationParams] = []

    async def __call__(self, params: LoggingMessageNotificationParams) -> None:
        print(params.data, end="")

logging_collector = LoggingCollector()

async def run():
    async with streamablehttp_client(
        "http://localhost:8000/mcp",
        headers={"Authorization": os.environ["AUTHORIZATION"]}) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
            logging_callback=logging_collector
        ) as session:
            await session.initialize()
            await session.call_tool(
                "streamable_llm_tool",
                arguments={"prompt": "写一个关于MCP在企业落地的技术报告"}
            )


if __name__ == "__main__":
    asyncio.run(run())
