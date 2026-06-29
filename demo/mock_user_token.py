from datetime import datetime, timedelta

import jwt
import os
import dotenv
dotenv.load_dotenv()


def generate_mock_token() -> str:
    user_info = {
        "sub": "kang99",
        "scopes": ["mcp:read", "mcp:write"],
        "exp": datetime(2026, 6, 30, 12, 0, 0) + timedelta(hours=1),
    }
    """Generate a JWT token for a user."""
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    token = jwt.encode(user_info, JWT_SECRET_KEY, algorithm="HS256")
    return token


if __name__ == "__main__":
    token = generate_mock_token()
    print(token)