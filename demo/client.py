import asyncio
import os
from fastmcp import Client


async def main():
    # # 连接stdio传输上的mcp服务
    # server_path = os.path.join(os.path.dirname(__file__), "server.py")
    # client = Client(server_path)
    client = Client("http://localhost:8000/mcp")# 连接http传输上的mcp服务
    async with client:
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f" - {tool.name}: {tool.description}")
        print("\n" + "=" * 50 + "\n")

        result = await client.call_tool(
            "get_weather",
            {"city": "Tokyo"}
        )
        print(f"Weather result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
