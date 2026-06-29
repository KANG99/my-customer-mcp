from mcp.server.fastmcp import FastMCP
from tools.weather import get_weather
from tools.time_tool import get_time
from tools.calculator import calculate
from tools.hello_user import get_username
from tools.resource import read_poem


mcp = FastMCP("my-first-server")

@mcp.tool()
def get_weather_tool(city: str) -> dict:
    """Get the current weather for a city."""
    return get_weather(city)

@mcp.tool()
def get_time_tool(timezone: str = None) -> str:
    """Get the current time."""
    return get_time(timezone)

@mcp.tool()
def calculate_tool(expression: str) -> int:
    """Calculate two numbers."""
    return calculate(expression)
    
@mcp.tool()
def get_username_tool() -> str:
    """Get the username of the current user."""
    return get_username()

@mcp.resource(uri="resource://resume/黄金叹", name="黄金叹.md", description="一首黄金叹，一把辛酸泪")
def poem_resource() -> str:
    """Get the content of the poem."""
    return read_poem()



if __name__ == "__main__":
    # mcp.run(transport="stdio")# 运行在stdio传输上
    mcp.run(transport="streamable-http")# 运行在streamable-http传输上
