import sys
import re
import json
import subprocess
from typing import Dict, List, Any, Union

def perform_web_search(query: str) -> List[Dict[str, str]]:
    """
    Use web search to find information about a real estate project.
    
    Args:
        query: The search query
        
    Returns:
        List of search result dictionaries
    """
    print(f"Searching for: {query}")
    
    try:
        # In a real implementation, you would use a search API
        # For this demonstration, we'll run a command that simulates a web search
        # Replace this with an actual API call in production
        command = ["python", "-c", f"print('Simulated web search for: {query}')"]
        
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running search command: {e}")
        
        # Mock search results (in a real implementation, these would come from the API)
        # Replace this with actual API results
        search_results = [
            {
                "title": "Luxury Apartments in Bangalore - Premium Project",
                "snippet": "Starting from ₹85 lakhs, these luxury apartments offer 2 BHK and 3 BHK configurations. Located in North Bangalore, developed by Premier Builders Group.",
                "url": "https://example.com/luxury-apartments"
            },
            {
                "title": "Premier Builders Group - Official Website",
                "snippet": "Premier Builders Group is a leading developer with over 15 years of experience. Current projects include luxury apartments in North Bangalore with 2-3 BHK options starting at ₹85 lakhs.",
                "url": "https://example.com/premier-builders"
            },
            {
                "title": "Real Estate Reviews - Luxury Apartments Project",
                "snippet": "The Luxury Apartments project offers units sized between 1200-1800 sq.ft. Located just 5 km from the airport in North Bangalore. Prices range from ₹85-120 lakhs depending on configuration.",
                "url": "https://example.com/reviews"
            }
        ]
        
        return search_results
        
    except Exception as e:
        print(f"Error in web search: {str(e)}")
        return []

def extract_facts(search_results: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """
    Extract facts about pricing, developer, location, and configuration
    from the search results.
    
    Args:
        search_results: List of search result dictionaries with title, snippet, and url
        
    Returns:
        Dictionary of categorized facts
    """
    facts = {
        "pricing": [],
        "developer": [],
        "location": [],
        "configuration": []
    }
    
    # Define regex patterns for each category
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
            r'(?:located|situated|placed)(?:\s+at|in)?\s+([A-Z][A-Za-z\s]+(?:,\s*[A-Za-z\s]+)?)',
            r'(?:at|in)\s+([A-Z][A-Za-z\s]+(?:,\s*[A-Za-z\s]+)?)'
        ],
        "configuration": [
            r'(\d+\s*BHK)',
            r'(\d+\s*bedroom)',
            r'(\d+(?:[,.]\d+)?\s*(?:sq\.?(?:\s*ft\.?)?|sqft|square\s*feet))'
        ]
    }
    
    # Process each search result
    for result in search_results:
        text = f"{result['title']} {result['snippet']}"
        
        # Check each category and its patterns
        for category, category_patterns in patterns.items():
            for pattern in category_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if match and str(match).strip() and match not in facts[category]:
                        facts[category].append(match)
    
    return facts

def format_results(facts: Dict[str, List[str]], search_results: List[Dict[str, str]]) -> str:
    """
    Format the search results and extracted facts.
    
    Args:
        facts: Dictionary of categorized facts
        search_results: Original search results
        
    Returns:
        Formatted string with search results and extracted facts
    """
    output = []
    
    # Add search results section
    output.append("Top 3 Relevant Snippets:")
    for i, result in enumerate(search_results[:3], 1):
        output.append(f"\n{i}. {result['title']}")
        output.append(f"   {result['snippet']}")
        output.append(f"   Source: {result['url']}")
    
    # Add facts summary section
    output.append("\nSummary of Facts:")
    
    if facts["pricing"]:
        output.append("\nPricing Information:")
        for price in facts["pricing"][:2]:  # Show top 2 results
            output.append(f"- Price point: {price}")
    
    if facts["developer"]:
        output.append("\nDeveloper Information:")
        for developer in facts["developer"][:2]:
            output.append(f"- Developer: {developer}")
    
    if facts["location"]:
        output.append("\nLocation Information:")
        for location in facts["location"][:2]:
            output.append(f"- Located in: {location}")
    
    if facts["configuration"]:
        output.append("\nConfiguration Information:")
        for config in facts["configuration"][:2]:
            output.append(f"- Unit type: {config}")
    
    # Check if we found any facts
    if not (facts["pricing"] or facts["developer"] or facts["location"] or facts["configuration"]):
        output.append("\nNo specific real estate facts were found in the search results.")
    
    return "\n".join(output)

def main():
    if len(sys.argv) < 2:
        print("Usage: python real_estate_web_search.py \"search query\"")
        return
    
    query = sys.argv[1]
    search_results = perform_web_search(query)
    
    if not search_results:
        print("No search results found.")
        return
    
    facts = extract_facts(search_results)
    formatted_output = format_results(facts, search_results)
    
    print(formatted_output)

if __name__ == "__main__":
    main() 