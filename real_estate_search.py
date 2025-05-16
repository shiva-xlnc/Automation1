import sys
import re
import requests
from bs4 import BeautifulSoup

def search_real_estate(query):
    """
    Search for real estate project information and return relevant snippets.
    This function will perform a web search and extract relevant information.
    """
    print(f"Searching for: {query}")
    
    try:
        # Using a search engine URL (this is for demonstration - in production use an API)
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers)
        
        if response.status_code != 200:
            return f"Error: Unable to perform search. Status code: {response.status_code}"
        
        # Parse search results
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        
        # Extract search result items (this will vary based on the search engine)
        result_elements = soup.select('div.g')
        
        for element in result_elements[:3]:  # Get top 3 results
            title_element = element.select_one('h3')
            snippet_element = element.select_one('div.IsZvec')
            link_element = element.select_one('a')
            
            if title_element and snippet_element and link_element:
                title = title_element.text
                snippet = snippet_element.text
                url = link_element.get('href')
                if url and url.startswith('/url?q='):
                    url = url.split('/url?q=')[1].split('&')[0]
                
                search_results.append({
                    'title': title,
                    'snippet': snippet,
                    'url': url
                })
        
        return search_results
    
    except Exception as e:
        return f"Error: {str(e)}"

def extract_facts(search_results):
    """
    Extract relevant facts about pricing, developer, location, and configuration
    from the search results.
    """
    if isinstance(search_results, str) and search_results.startswith("Error"):
        return search_results
    
    facts = {
        "pricing": [],
        "developer": [],
        "location": [],
        "configuration": []
    }
    
    price_patterns = [
        r'(?:starting|price|from)[^\d]*(?:₹|Rs\.?|INR)?[^\d]*(\d+(?:[,.]\d+)?)\s*(?:lakhs?|lacs?|crores?|L|Cr)',
        r'(?:₹|Rs\.?|INR)\s*(\d+(?:[,.]\d+)?)\s*(?:lakhs?|lacs?|crores?|L|Cr)',
        r'(\d+(?:[,.]\d+)?)\s*(?:lakhs?|lacs?|crores?|L|Cr)'
    ]
    
    developer_patterns = [
        r'(?:developed|developer|built|constructed)(?:\s+by)?\s+([A-Z][A-Za-z\s]+(?:Developers|Properties|Builders|Group|Realty|Construction))',
        r'([A-Z][A-Za-z\s]+(?:Developers|Properties|Builders|Group|Realty|Construction))'
    ]
    
    location_patterns = [
        r'(?:located|situated|placed)(?:\s+at|in)?\s+([A-Z][A-Za-z\s]+,\s*[A-Za-z\s]+)',
        r'(?:at|in)\s+([A-Z][A-Za-z\s]+(?:,\s*[A-Za-z\s]+)?)'
    ]
    
    config_patterns = [
        r'(\d+\s*BHK)',
        r'(\d+\s*bedroom)',
        r'(\d+(?:[,.]\d+)?\s*(?:sq\.?(?:\s*ft\.?)?|sqft|square\s*feet))'
    ]
    
    for result in search_results:
        snippet = result["snippet"]
        
        # Extract pricing information
        for pattern in price_patterns:
            matches = re.findall(pattern, snippet, re.IGNORECASE)
            if matches:
                for match in matches:
                    facts["pricing"].append(f"Price information: {match} found in context: '{snippet[:100]}...'")
        
        # Extract developer information
        for pattern in developer_patterns:
            matches = re.findall(pattern, snippet, re.IGNORECASE)
            if matches:
                for match in matches:
                    facts["developer"].append(f"Developer information: {match} found in context: '{snippet[:100]}...'")
        
        # Extract location information
        for pattern in location_patterns:
            matches = re.findall(pattern, snippet, re.IGNORECASE)
            if matches:
                for match in matches:
                    facts["location"].append(f"Location information: {match} found in context: '{snippet[:100]}...'")
        
        # Extract configuration information
        for pattern in config_patterns:
            matches = re.findall(pattern, snippet, re.IGNORECASE)
            if matches:
                for match in matches:
                    facts["configuration"].append(f"Configuration information: {match} found in context: '{snippet[:100]}...'")
    
    return facts

def summarize_facts(facts):
    """
    Create a summary of the facts found.
    """
    if isinstance(facts, str) and facts.startswith("Error"):
        return facts
    
    summary = []
    
    for category, info_list in facts.items():
        if info_list:
            summary.append(f"\n{category.title()} Information:")
            for i, info in enumerate(info_list[:2], 1):  # Limit to top 2 findings per category
                summary.append(f"  {i}. {info}")
    
    if not summary:
        return "No relevant information found in the search results."
    
    return "\n".join(summary)

def main():
    if len(sys.argv) < 2:
        print("Usage: python real_estate_search.py \"search query\"")
        return
    
    query = sys.argv[1]
    results = search_real_estate(query)
    
    if isinstance(results, str) and results.startswith("Error"):
        print(results)
        return
    
    print("\nTop 3 Relevant Search Results:")
    for i, result in enumerate(results[:3], 1):
        print(f"\n{i}. {result['title']}")
        print(f"   {result['snippet'][:200]}...")
        print(f"   Source: {result['url']}")
    
    facts = extract_facts(results)
    summary = summarize_facts(facts)
    
    print("\nSummary of Relevant Real Estate Facts:")
    print(summary)

if __name__ == "__main__":
    main() 