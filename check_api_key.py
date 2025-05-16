import os

def check_serpapi_key():
    api_key = os.getenv("SERPAPI_API_KEY")
    if api_key:
        print("✅ SERPAPI_API_KEY is set.")
        # Optional: For security, don't print the full key; just the first 4 chars
        print(f"Key preview: {api_key[:4]}{'*' * (len(api_key) - 4)}")
    else:
        print("❌ SERPAPI_API_KEY is NOT set.")
        print("Please set the environment variable before running your script.")

if __name__ == "__main__":
    check_serpapi_key()
