from datetime import timedelta, datetime, UTC
import os

import jwt


def create_jwt(data: dict, expire_delta: timedelta | None = None) -> str:
    """
    Create and sign a JWT access token.
    
    Encodes custom data into a JWT token with optional expiration time.
    If expire_delta is not provided, uses JWT_EXPIRATION_TIME_MINUTES from environment.
    
    Args:
        data (dict): Custom data to store in token (typically {"sub": email})
        expire_delta (timedelta | None): Time delta for token expiration. If None,
            uses JWT_EXPIRATION_TIME_MINUTES environment variable. Defaults to None.
    
    Returns:
        str: Signed JWT token
    """
    to_encode = data.copy()
    
    if expire_delta:
        expire = datetime.now(tz=UTC) + expire_delta
    else:
        expire = datetime.now(tz=UTC) + timedelta(minutes=int(os.getenv("JWT_EXPIRATION_TIME_MINUTES", 30)))
    
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")