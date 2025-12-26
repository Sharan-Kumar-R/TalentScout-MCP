from mcp.server.fastmcp import FastMCP
from linkedin_client import LinkedInClient
import json

# Initialize the MCP Server
mcp = FastMCP("HR-Agent-LinkedIn")

# Initialize LinkedIn Client
li_client = LinkedInClient()

@mcp.tool()
def search_candidates(keywords: str, location: str | None = None, limit: int = 5) -> str:
    """
    Search for candidates on LinkedIn.
    
    Args:
        keywords: Search terms (e.g., "Python Developer", "Data Scientist")
        location: Location filter (e.g., "San Francisco", "Remote")
        limit: Number of results to return (default: 5)
    """
    try:
        results = li_client.search_people(keywords, location, limit)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def search_jobs(keywords: str, location: str | None = None, limit: int = 5) -> str:
    """
    Search for jobs on LinkedIn.
    
    Args:
        keywords: Job title or keywords
        location: Location name
        limit: Number of results to return
    """
    try:
        results = li_client.search_jobs(keywords, location, limit)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_candidate_profile(urn_id: str) -> str:
    """
    Get detailed profile for a candidate using their URN ID (public_id).
    
    Args:
        urn_id: The unique identifier for the profile (often found in search results)
    """
    try:
        profile = li_client.get_profile(urn_id)
        if profile:
            return json.dumps(profile, indent=2)
        return "Profile not found."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
