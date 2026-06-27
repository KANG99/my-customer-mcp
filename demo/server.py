from fastmcp import FastMCP
from tools.weather import get_weather
from tools.time_tool import get_time
from tools.calculator import calculate


mcp = FastMCP("my-first-server")

mcp.tool(get_weather)
mcp.tool(get_time)
mcp.tool(calculate)


if __name__ == "__main__":
    # mcp.run(transport="stdio")# 运行在stdio传输上
    mcp.run(transport="http",host="0.0.0.0", port=8000)# 运行在http传输上
