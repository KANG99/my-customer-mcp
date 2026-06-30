from mcp.server.fastmcp import FastMCP, Context
from mcp.server.auth.settings import AuthSettings

from tools.weather import get_weather
from tools.time_tool import get_time
from tools.calculator import calculate
from tools.hello_user import get_username
from tools.resource import read_poem
from tools.sampling import generate_task
from tools.streamable_llm import streamable_llm


from prompts.prompts_templates import doc_experts_prompt

from server_auth import CustomerTokenVerifier

mcp = FastMCP("my-first-server",
     token_verifier=CustomerTokenVerifier(),
     auth=AuthSettings(
          issuer_url="http://localhost:8000", # 令牌签发者地址（本服务地址）
          resource_server_url="http://localhost:8000", # 当前MCP服务地址
          required_scopes=["mcp:read", "mcp:write"], # 强制要求客户端必须拥有这两个权限
          )
     )

@mcp.tool()
def get_weather_tool(city: str) -> dict:
    """
    Get the current weather for a city.
    Args:
        city: 城市名称，如 "New York"、"London"、"Tokyo" 等。
    
    Returns:
        包含城市、温度和天气条件的字典，如 {"city": "New York", "temp": 72, "condition": "sunny"}。
    """
    return get_weather(city)

@mcp.tool()
def get_time_tool(timezone: str = "UTC") -> str:
    """
    Get the current time for a given timezone.
    
    Args:
        timezone: IANA 时区名称，默认为 UTC（时区名称例如 Asia/Shanghai、America/New_York）。
    
    Returns:
        格式化后的时间字符串，如 "Current time (Asia/Shanghai): 14:09:14"。
    """
    return get_time(timezone)

@mcp.tool()
def calculate_tool(expression: str) -> int:
    """
    Calculate two numbers.
    
    Args:
        expression: 包含两个数字和运算符的字符串，如 "2 + 3"。
    
    Returns:
        计算结果，如 5。
    """
    return calculate(expression)
    
@mcp.tool()
def get_username_tool() -> str:
    """
    Get the username of the current user.
    Returns:
        当前用户的用户名，如 "user123"。
    """
    return get_username()

@mcp.resource(uri="resource://resume/黄金叹", name="黄金叹.md", description="一首黄金叹，一把辛酸泪")
def poem_resource() -> str:
    """Get the content of the poem."""
    return read_poem()

@mcp.prompt(name="doc_experts",description="文本校对模版")
def doc_experts_tool(task: str) -> str:
    """Get the content of the poem."""
    return doc_experts_prompt.format(task=task)

@mcp.tool()
async def generate_task_tool(topic: str, ctx: Context) -> str:
    """Generate a task for a given topic."""
    return await generate_task(topic, ctx)

@mcp.tool()
async def streamable_llm_tool(prompt: str, ctx: Context) -> str:
    """Stream a response from a given prompt."""
    return await streamable_llm(prompt, ctx)


if __name__ == "__main__":
    # mcp.run(transport="stdio")# 运行在stdio传输上
    mcp.run(transport="streamable-http")# 运行在streamable-http传输上
