from mcp.server.fastmcp import Context
from openai import AsyncOpenAI


model_name = "qwen3.6:35b-mlx"
client = AsyncOpenAI(api_key='no-sk-required',
                    base_url="http://127.0.0.1:11434/v1",
)

async def streamable_llm(prompt: str, ctx: Context) -> str:

    response = await client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        stream=True
    )

    async for chunk in response:
        if chunk.choices[0].delta.content:
            await ctx.info(chunk.choices[0].delta.content)
    return "completed"