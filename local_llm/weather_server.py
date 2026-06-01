from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


@mcp.tool()
async def search_location(query: str) -> dict:
    return {
        "city": query,
        "location_key": "208971"
    }


@mcp.tool()
async def get_current_weather(location_key: str) -> dict:
    return {
        "location_key": location_key,
        "weather": "Sunny",
        "temperature": 32
    }


if __name__ == "__main__":
    mcp.run()