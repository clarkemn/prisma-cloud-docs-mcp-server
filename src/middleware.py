"""
Custom middleware for Smithery configuration handling in FastMCP HTTP mode.
This middleware processes Smithery session configuration and makes it available to tools.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SmitheryConfigMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts and processes Smithery configuration from requests.
    
    In Smithery's HTTP mode, configuration is passed via request headers or body.
    This middleware makes the config accessible to MCP tools via request context.
    """
    
    async def dispatch(self, request: Request, call_next):
        # Extract Smithery configuration from request
        config = await self._extract_config(request)
        
        # Store config in request state for tools to access
        request.state.smithery_config = config
        
        # Log configuration for debugging (remove in production)
        if config:
            logger.debug(f"Smithery config loaded: {list(config.keys())}")
        
        response = await call_next(request)
        return response
    
    async def _extract_config(self, request: Request) -> Dict[str, Any]:
        """
        Extract Smithery configuration from the request.
        
        Smithery can pass config via:
        1. X-Smithery-Config header (JSON string)
        2. Request body (for POST requests with config)
        3. Query parameters
        """
        config = {}
        
        # Method 1: Check for Smithery config header
        config_header = request.headers.get("x-smithery-config")
        if config_header:
            try:
                config.update(json.loads(config_header))
            except json.JSONDecodeError:
                logger.warning("Invalid JSON in x-smithery-config header")
        
        # Method 2: Check for config in request body (if POST/PUT)
        if request.method in ["POST", "PUT"]:
            try:
                # Read body without consuming it (for FastMCP to process later)
                body = await request.body()
                if body:
                    # Try to extract config from JSON body
                    body_data = json.loads(body.decode())
                    if isinstance(body_data, dict) and "config" in body_data:
                        config.update(body_data["config"])
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Not JSON or not decodable, skip
                pass
        
        # Method 3: Query parameters (less common but supported)
        for key, value in request.query_params.items():
            if key.startswith("config_"):
                config_key = key[7:]  # Remove "config_" prefix
                config[config_key] = value
        
        return config

def get_config_from_request(request: Request) -> Dict[str, Any]:
    """
    Utility function for tools to get Smithery configuration from request context.
    
    Usage in tools:
        from starlette.requests import Request
        from src.middleware import get_config_from_request
        
        @mcp.tool()
        async def my_tool(request: Request = None):
            config = get_config_from_request(request) if request else {}
            api_key = config.get('api_key', 'default_key')
            # Use config...
    """
    if hasattr(request, 'state') and hasattr(request.state, 'smithery_config'):
        return request.state.smithery_config
    return {}

# Example configuration schema for reference
EXAMPLE_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "api_key": {
            "type": "string",
            "description": "API key for external services"
        },
        "max_pages": {
            "type": "integer", 
            "description": "Maximum pages to index",
            "default": 50
        },
        "cache_ttl": {
            "type": "integer",
            "description": "Cache TTL in seconds",
            "default": 3600
        }
    }
}