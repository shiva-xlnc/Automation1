import os
import sys
import re
from serpapi import GoogleSearch

def search_web(query):
    """
    Performs a Google search using SerpAPI and returns top results.
    
    Args:
        query (str): Search query string
        
    Returns:
        list: List of dictionaries containing search results with title, snippet, and URL
    """
    # Get API key from environment variable or use fallback
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        api_key = "e04d78d2ef066ab7affc20cd1242519daff2552214090676d1b4976d705cc697"
        print("Warning: Using fallback API key. Set SERPAPI_API_KEY for your own key.")
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 3  # Limit to 3 results to minimize API usage
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "organic_results" not in results:
            print("No search results found.")
            return []
        
        search_results = []
        for r in results["organic_results"][:3]:  # Ensure we only take top 3
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
    Extracts real estate information from search results.
    
    Args:
        search_results (list): List of search result dictionaries
        
    Returns:
        dict: Dictionary with categorized real estate information
    """
    info = {
        "pricing": [],
        "developer": [],
        "location": [],
        "configuration": []
    }
    
    # Define regex patterns to extract information
    patterns = {
        "pricing": [
            r'(?:starting|price|from)[^\d]*(?:₹|Rs\.?|INR)?[^\d]*(\d+(?:[,.]\d+)?)\s*(?:lakhs?|lacs?|crores?|L|Cr)',
            r'(?:₹|Rs\.?|INR)\s*(\d+(?:[,.]\d+)?)\s*(?:lakhs?|lacs?|crores?|L|Cr)',
            r'(\d+(?:[,.]\d+)?)\s*(?:lakhs?|lacs?|crores?|L|Cr)'
        ],
        "developer": [
            r'(?:developed|developer|built|constructed)(?:\s+by)?\s+([A-Z][A-Za-z\s]+(?:Developers|Properties|Builders|Group|Realty|Construction))',
            r'([A-Z][A-Za-z\s]+(?:Developers|Properties|Builders|Group|Realty|Construction))'
        ],
        "location": [
            r'(?:located|situated|placed)(?:\s+in|at)?\s+([A-Za-z\s]+(?:Bangalore|Chennai|Mumbai|Delhi|Kolkata|Hyderabad|Pune|Ahmedabad))',
            r'(?:in|at)\s+([A-Za-z\s]+(?:Bangalore|Chennai|Mumbai|Delhi|Kolkata|Hyderabad|Pune|Ahmedabad))',
            r'(?:in|at)\s+([A-Za-z\s]+(?:East|West|North|South|Central)[A-Za-z\s]+)'
        ],
        "configuration": [
            r'(\d+\s*BHK)',
            r'(\d+\s*bedroom)',
            r'(\d+(?:[,.]\d+)?\s*(?:sq\.?(?:\s*ft\.?)?|sqft|square\s*feet))'
        ]
    }
    
    # Process each search result
    for result in search_results:
        combined_text = f"{result['title']} {result['snippet']}"
        
        # Check each category and its patterns
        for category, category_patterns in patterns.items():
            for pattern in category_patterns:
                matches = re.findall(pattern, combined_text, re.IGNORECASE)
                for match in matches:
                    if match and str(match).strip() and match not in info[category]:
                        info[category].append(match)
    
    return info

def format_results(search_results, extracted_info):
    """
    Format search results and extracted information.
    
    Args:
        search_results (list): List of search result dictionaries
        extracted_info (dict): Dictionary with categorized real estate information
        
    Returns:
        str: Formatted output string
    """
    output = []
    
    # Add search results section
    output.append("Top Relevant Snippets:")
    for i, result in enumerate(search_results, 1):
        output.append(f"\n{i}. {result['title']}")
        output.append(f"   {result['snippet']}")
        output.append(f"   Source: {result['url']}")
    
    # Add extracted information section
    output.append("\nExtracted Real Estate Information:")
    
    if extracted_info["pricing"]:
        output.append("\nPricing Information:")
        for price in extracted_info["pricing"][:2]:  # Limit to 2 entries
            output.append(f"- {price}")
    
    if extracted_info["developer"]:
        output.append("\nDeveloper Information:")
        for developer in extracted_info["developer"][:2]:
            output.append(f"- {developer}")
    
    if extracted_info["location"]:
        output.append("\nLocation Information:")
        for location in extracted_info["location"][:2]:
            output.append(f"- {location}")
    
    if extracted_info["configuration"]:
        output.append("\nConfiguration Information:")
        for config in extracted_info["configuration"][:2]:
            output.append(f"- {config}")
    
    if not any(extracted_info.values()):
        output.append("\nNo specific real estate information could be extracted from the search results.")
    
    return "\n".join(output)

def main():
    if len(sys.argv) < 2:
        print("Usage: python real_estate_serpapi.py \"search query\"")
        print("\nExample searches:")
        print("  \"Prestige City Bangalore price\"")
        print("  \"Godrej Properties Mumbai flats\"")
        print("  \"DLF Gurgaon 3BHK\"")
        sys.exit(1)
    
    query = sys.argv[1]
    print(f"Searching for: {query}")
    
    # Perform search
    search_results = search_web(query)
    
    if not search_results:
        print("No results found or error occurred during search.")
        sys.exit(1)
    
    # Extract real estate information
    extracted_info = extract_real_estate_info(search_results)
    
    # Format and print results
    formatted_output = format_results(search_results, extracted_info)
    print(formatted_output)

if __name__ == "__main__":
    main() 