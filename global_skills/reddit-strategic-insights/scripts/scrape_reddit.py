import sys
import json

# This script coordinates with exa-mcp-server
def get_reddit_insights_exa(query):
    print(f"Triggering Exa Neural Search for: {query}")
    print("Filter: domain=reddit.com")
    
    # Exa search logic would go here via MCP call
    # results = exa.search(query, include_domains=["reddit.com"], num_results=5)
    
    # Structured response for the CEO
    return {
        "engine": "Exa Neural",
        "query": query,
        "results": "Pending MCP Execution"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        print(json.dumps(get_reddit_insights_exa(query), indent=2))