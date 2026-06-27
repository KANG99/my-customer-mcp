from fastmcp import FastMCP
from tools.weather import get_weather
from tools.time_tool import get_time
from tools.calculator import calculate
from tools.hello_user import get_username
from tools.resource import read_resume


mcp = FastMCP("my-first-server")

mcp.tool(get_weather)
mcp.tool(get_time)
mcp.tool(calculate)
mcp.tool(get_username)
mcp.resource(
     "resource://resume/黄金叹",
     name="黄金叹.md",
     description="本地 Markdown 文件内容示例",
)(read_resume)


if __name__ == "__main__":
    # mcp.run(transport="stdio")# 运行在stdio传输上
    mcp.run(transport="http",host="0.0.0.0", port=8000)# 运行在http传输上
