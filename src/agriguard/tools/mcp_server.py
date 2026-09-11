"""FastMCP registration for stable AgriGuard tools."""
from agriguard.settings import get_settings
from agriguard.rag import SQLiteVectorStore
from agriguard.tools.weather_tool import get_weather
from agriguard.tools.knowledge_tool import search_crop_guidance

try:
    from fastmcp import FastMCP
    mcp=FastMCP('AgriGuard AI Tools')
    @mcp.tool
    def weather_lookup(location:str)->dict:"""Return current spray-relevant weather.""";return get_weather(location)
    @mcp.tool
    def crop_knowledge_search(crop:str,symptoms:str,stage:str='')->list[dict]:
        """Return ranked chunks from the approved knowledge base."""
        s=get_settings();return search_crop_guidance(SQLiteVectorStore(s.database_path),crop,symptoms,stage)
except ImportError:mcp=None

if __name__=='__main__':
    if mcp is None:raise SystemExit('Install fastmcp to run the MCP server.')
    mcp.run()
