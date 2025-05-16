# Real Estate Search Tools

This repository contains scripts for searching and extracting information about real estate projects.

## Requirements

Install the required packages:

```
pip install -r requirements.txt
```

## Available Scripts

### 1. search_real_estate.py

A simple script that simulates searching for real estate information and extracts facts from mock data.

**Usage:**

```
python search_real_estate.py "Your search query"
```

### 2. real_estate_search.py

A more advanced script that attempts to perform actual web searches (note: web scraping may be subject to limitations).

**Usage:**

```
python real_estate_search.py "Project Name Location starting price"
```

### 3. real_estate_facts.py

A script that demonstrates how to extract and categorize real estate information from search results.

**Usage:**

```
python real_estate_facts.py "Developer name Project Name official website"
```

### 4. real_estate_web_search.py

A script that simulates web search using subprocess commands.

**Usage:**

```
python real_estate_web_search.py "Unit configuration in Project Name Location"
```

### 5. real_estate_search_tool.py

Implementation using argument parsing with improved regex patterns.

**Usage:**

```
python real_estate_search_tool.py "Prestige City East Bangalore pricing"
```

### 6. serpapi_search.py

Basic implementation of SerpAPI for real web searches.

**Usage:**

```
python serpapi_search.py "Your search query"
```

### 7. real_estate_serpapi.py

The most complete and functional implementation using SerpAPI for real search results and extracting real estate information.

**Usage:**

```
python real_estate_serpapi.py "Prestige City Bangalore price"
```

Before using SerpAPI scripts, set your API key (Windows PowerShell):

```
$env:SERPAPI_API_KEY = "your_api_key_here"
```

## Example Search Queries

To get good results, use queries that include specific information:

1. "Project Name in Location starting price"
2. "Developer name official project site"
3. "Unit configuration in Project Name Location"

## Information Extracted

The scripts extract the following types of information:

1. **Pricing** - Starting prices, price ranges, etc.
2. **Developer** - The company developing the project
3. **Location** - Where the project is located
4. **Configuration** - Unit types, sizes, layouts (e.g., 2BHK, 3BHK, square footage)

## Setting Up a Virtual Environment

### Windows

```
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Linux/macOS

```
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```
