import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi_mcp import FastApiMCP
from pyfiglet import Figlet

app = FastAPI()

async def verify_token(authorization: str | None = Header(None)):
    valid_tokens = {"token123", "token456"}
    if authorization not in valid_tokens:
        raise HTTPException(status_code=403, detail="错误的Token")
    return True

@app.get("/figlet", operation_id="figlet")
async def figlet(text: str, is_auth: bool = Depends(verify_token)):
    f = Figlet(font='block')
    result = f.renderText(text)

    if result is None:
        return text
    else:
        return result

mcp = FastApiMCP(app)
mcp.mount()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7861)