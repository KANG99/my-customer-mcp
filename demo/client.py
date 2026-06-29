import asyncio
from fastmcp import Client
from mock_user_token import generate_mock_token


async def main():
    client = Client("http://localhost:8000/mcp",auth=generate_mock_token())  # 连接http传输上的mcp服务
    async with client:
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f" - {tool.name}: {tool.description}")
        print("\n" + "=" * 50 + "\n")

        result = await client.call_tool(
              "get_weather_tool",
              {"city": "Tokyo"}
          )
        print(f"Weather result: {result}")

        # --- Resources example ---
        resources = await client.list_resources()
        print("\n" + "=" * 50)
        print("Available resources:")
        for r in resources:
            print(f" - {r.uri}: {r.description or '(no description)'}")
        print("\n" + "=" * 50 + "\n")

        contents = await client.read_resource("resource://resume/黄金叹")
        print("Resource content:")
        for c in contents:
            print(c.text if hasattr(c, "text") else c)


if __name__ == "__main__":
    asyncio.run(main())
