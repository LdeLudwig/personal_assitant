import json

from personal_notion_agent.infrastructure.settings import get_settings

from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters


async def notion_mcp_tool():
    settings = get_settings()
    
    api_key = settings.notion_api_key
    
    if not api_key:
        raise ValueError(
            "Missing Notion API key: provide --NOTION_API_KEY or set NOTION_API_KEY environment variable"
        )
        
    command = "npx"
    args = ["-y", "@notionhq/notion-mcp-server"]
    env = {
        "OPENAPI_MCP_HEADERS": json.dumps(
            {"Authorization": f"Bearer {api_key}"}
        )
    }
    
    server_params = StdioServerParameters(command=command, args=args, env=env)
    
    notion_mcp_tool = MCPTools(server_params=server_params)
    
    return notion_mcp_tool