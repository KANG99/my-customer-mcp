"""单次调用示例: 让本地 LLM 自主发现并调用 MCP 服务中的 get_time.

运行前:
    1. 启动 MCP 服务: python demo/server.py (在 http://0.0.0.0:8000/mcp)
    2. 确保 Ollama 模型可用: ollama list | grep qwen3-coder

运行:
    python demo/mcp_llm_demo_single.py

核心流程:
    1. MCPClient 连接你的服务, 拿到工具定义 (非硬编码)
    2. bind_tools 将工具转为 Ollama function calling 格式
    3. LLM 自主决定调用哪个工具 + 参数
    4. 你执行实际 MCP 工具的逻辑, 把结果返回给 LLM
"""

import asyncio
import json
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama

from mock_user_token import generate_mock_token


class McpToolExecutor:
    # 执行器: LLM 选择工具后, 这里实际调用你的 MCP 服务

    def __init__(self) -> None:
        self.client = MultiServerMCPClient({
             "my-mcp-server": {
                 "transport": "streamable-http",
                 "url": "http://localhost:8000/mcp",
                 "headers": {"Authorization": f'Bearer {generate_mock_token()}'},
             },
         })
        self.tools_map: dict[str, Any] | None = {}

    async def initialize(self) -> None:
         # 加载所有 MCP 工具
        tools = await self.client.get_tools()
        for tool in tools:
            self.tools_map[tool.name] = tool

    async def execute(self, name: str, args: dict[str, Any]) -> str:
         # 通过 MCP 服务执行工具
        tool = self.tools_map[name]   # type: ignore[index]
        result = await tool.ainvoke(args)
        if hasattr(result, "content"):
            return str(
                result.content[0].text
                if isinstance(result.content, list)
                else result.content
             )
        return str(result)


async def demo_single() -> None:
     # 1. 获取 MCP 服务提供的工具 (非硬编码!)
    executor = McpToolExecutor()
    await executor.initialize()

     # 2. 构建 LLM 可见的工具定义 (LLM 自主发现, 不是写死的)
    tool_defs = [
         {
             "type": "function",
             "function": {
                 "name": t.name,
                 "description": t.description,
                 "parameters": getattr(t, "inputSchema", {}).get("properties", {}) or {},
             },
         }
        for t in executor.tools_map.values()   # type: ignore[attr-defined]
     ]

    print("LLM 看到的工具定义 (自主发现):")
    for td in tool_defs:
        fn = td["function"]
        print(f"    - {fn['name']}: {fn['description']}")

     # 3. 创建 LLM + tools, 让模型决定何时调用
    llm_with_tools = ChatOllama(
        model="qwen3.6:35b-mlx",
        temperature=0.7,
        max_tokens=4096,
        top_p=0.80, 
        top_k=20,  
        # reasoning=False,
     ).bind_tools(tool_defs)

     # ---------- 示例 A: LLM 自主调用 get_time ----------
    print("\n--- 示例 A: 查询时间 (LLM 自主发现并调用) ---")
    messages_a = [HumanMessage(content="国内现在几点了?")]
    response_a = await llm_with_tools.ainvoke(messages_a)

     # 检查 LLM 是否调用了工具
    tool_calls_a = getattr(response_a, "tool_calls", [])
    if tool_calls_a:
        for tc in tool_calls_a:
            name = tc["name"]
            args_dict = tc.get("args", {})   # type: ignore[union-attr]
            print(f"LLM 选择调用: {name}")
            print(f"参数: {json.dumps(args_dict, ensure_ascii=False)}")

             # 实际执行 MCP 工具
            if name in executor.tools_map:
                tool_result = await executor.execute(name, args_dict)   # type: ignore[arg-type]
                print(f"MCP 服务返回: {tool_result}")

                 # 将结果反馈给 LLM
                messages_a.append(AIMessage(
                    content=response_a.content,
                    tool_calls=tool_calls_a,
                 ))
                messages_a.append(HumanMessage(
                    content=f"工具 [{name}] 返回: {tool_result}"
                 ))
                final_response = await llm_with_tools.ainvoke(messages_a)
                print(f"\nLLM 最终回复:\n{final_response.content}")
            else:
                print(f"未知工具: {name}")
    else:
        print(f"LLM 直接回复 (未调用工具):\n{response_a.content}")

     # ---------- 示例 B: 组合任务, LLM 调用多个工具 ----------
    print("\n--- 示例 B: 组合任务 (LLM 自主决定调用多个工具) ---")
    messages_b = [HumanMessage(
        content="告诉我我的用户名是什么,现在北京是几点?"
     )]
    response_b = await llm_with_tools.ainvoke(messages_b)
    tool_calls_b = getattr(response_b, "tool_calls", [])
    if tool_calls_b:
        print("LLM 调用了多个工具:")
        for tc in tool_calls_b:
            name = tc["name"]
            args_dict = tc.get("args", {})   # type: ignore[arg-type]
            print(f"  - {name}: {json.dumps(args_dict, ensure_ascii=False)}")

             # 执行所有工具调用
        all_results = []
        for tc in tool_calls_b:
            name = tc["name"]
            args_dict = tc.get("args", {})   # type: ignore[arg-type]
            if name in executor.tools_map:
                result = await executor.execute(name, args_dict)
                all_results.append(f"{name}: {result}")
                print(f"  MCP 返回: {result}")

                 # 反馈给 LLM
                messages_b.append(AIMessage(
                    content=response_b.content,
                    tool_calls=tool_calls_b,
                 ))
                messages_b.append(HumanMessage(
                    content=f"工具 [{name}] 返回: {all_results[-1]}"
                 ))

        if all_results:
              # 将工具结果反馈给 LLM, 让它综合回复
            final_response = await llm_with_tools.ainvoke(messages_b)
            print(f"\nLLM 最终回复:\n{final_response.content}")
    else:
        print(f"LLM 直接回复:\n{response_b.content}")


if __name__ == "__main__":
    asyncio.run(demo_single())
