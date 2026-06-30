import os
import dotenv
dotenv.load_dotenv()

import jwt
from mcp.server.auth.provider import TokenVerifier, AccessToken
from mcp.server.auth.settings import AuthSettings
from datetime import datetime, timedelta

class CustomerTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken:
        """Verify the token and return the user information."""
        try:
            payload = jwt.decode(token, os.environ["JWT_SECRET_KEY"], algorithms=["HS256"])
            return AccessToken(token=token, client_id=payload["sub"], scopes=payload["scopes"], expires=payload["exp"])
        except jwt.exceptions.DecodeError:
            return None  

    

if __name__ == "__main__":
    ...