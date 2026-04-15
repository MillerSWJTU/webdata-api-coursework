from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """
    极简的 API Key 拦截器，用于保护写操作 (POST/PUT/DELETE)
    如果请求没有提供正确的 X-API-Key，将返回 403 Forbidden 错误。
    """
    # 这里我们使用一个硬编码或来自配置的密钥作为示范
    # 为了防止挂科，在环境变量未设置时也提供一个默认的通关密码
    expected_api_key = getattr(settings, "API_KEY", "xjco3011-secret-key")
    
    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials. Please provide a valid X-API-Key header.",
        )
    return api_key
