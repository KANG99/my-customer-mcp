from mcp.server.fastmcp import Context
from mcp.types import SamplingMessage, TextContent


async def generate_task(topic: str, ctx: Context) -> str:
    prompt = f"create a plan for {topic}"

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt),
            )
        ],
        max_tokens=100,
    )

    if result.content.type == "text":
        return result.content.text
    return str(result.content)
