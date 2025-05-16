import os
import sys
from serpapi import GoogleSearch

def search_web(query):
    """
    Performs a Google search using SerpAPI and returns top results.
    
    Args:
        query (str): Search query string
        
    Returns:
        list: List of dictionaries containing search results with title, snippet, and URL
        
    Raises:
        ValueError: If SERPAPI_API_KEY environment variable is not set
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable not set.")
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 3
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "organic_results" not in results:
            print("No search results found.")
            return []
        
        search_results = []
        for r in results["organic_results"]:
            search_results.append({
                "title": r.get("title", ""),
                "snippet": r.get("snippet", ""),
                "url": r.get("link", "")
            })
        return search_results
    
    except Exception as e:
        print(f"Error during search: {e}")
        return []

def extract_real_estate_info(search_results):
    """
    Extracts real estate specific information from search results.
    This is a placeholder for future implementation.
    
    Args:
        search_results (list): List of search result dictionaries
        
    Returns:
        dict: Dictionary with categorized real estate information
    """
    # Placeholder for real estate information extraction
    # In a complete implementation, this would use regex patterns to extract
    # price, developer, location, and configuration information
    return {
        "pricing": [],
        "developer": [],
        "location": [],
        "configuration": []
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python serpapi_search.py \"search query\"")
        sys.exit(1)

    query = sys.argv[1]
    print(f"Searching for: {query}")
    
    results = search_web(query)

    if not results:
        print("No results found.")
    else:
        print("\nSearch Results:")
        for idx, res in enumerate(results, 1):
            print(f"\nResult {idx}:")
            print(f"Title: {res['title']}")
            print(f"Snippet: {res['snippet']}")
            print(f"URL: {res['url']}")
        
        # You can add this line if you want to extract real estate info in the future
        # info = extract_real_estate_info(results)
        # print("\nExtracted Real Estate Information:", info) 