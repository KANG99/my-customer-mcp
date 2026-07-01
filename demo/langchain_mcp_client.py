import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen3.6:35b-mlx",
    base_url="http://127.0.0.1:11434/v1",
    openai_api_key="no-sk-required"
)

mcpserver_url = "http://127.0.0.1:7860/gradio_api/mcp/http"

async def run():
    async with streamablehttp_client(mcpserver_url) \
            as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_agent(model=llm, tools=tools)
            response = await agent.ainvoke(
                {"messages":
                    "大语言模型和大型语言模型是不是一个意思？" +
                    "用工具计算它们之间的文本相似度。"}
            )
            messages = response.get("messages", [])
            if messages:
                print(messages[-1].content)
            else:
                print("No messages in response")

if __name__ == "__main__":
    asyncio.run(run())