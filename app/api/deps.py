from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """
    Minimal API Key interceptor to protect write operations (POST/PUT/DELETE).
    Returns 403 Forbidden if the request does not provide a valid X-API-Key.
    """
    expected_api_key = settings.api_key
    
    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials. Please provide a valid X-API-Key header.",
        )
    return api_key
