def google_search(query: str, num_results: int = 2, max_chars: int = 500) -> list:
    """
    Perform a Google search and return enriched results including titles, links, snippets, and body content.
    First, display all the links before showing the enriched details.
    
    :param query: The search query string.
    :param num_results: Number of results to fetch (default: 2).
    :param max_chars: Maximum number of characters to retrieve from the body of each link (default: 500).
    :return: A list of dictionaries with enriched search results.
    """
    # Necessary imports inside the function
    import os
    import time
    import requests
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv

    # Load API credentials from the .env file
    load_dotenv()

    # Retrieve API Key and Search Engine ID
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    # Check if the credentials are available
    if not api_key or not search_engine_id:
        raise ValueError("API key or Search Engine ID not found in environment variables")

    # Google Custom Search API endpoint
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": search_engine_id, "q": query, "num": num_results}

    # Perform the API request
    response = requests.get(url, params=params)

    # Check for errors in the response
    if response.status_code != 200:
        print(response.json())
        raise Exception(f"Error in API request: {response.status_code}")

    # Parse the API response
    results = response.json().get("items", [])

    # Show all links first
    print("\nAll Links:")
    links = [item["link"] for item in results]
    for idx, link in enumerate(links, start=1):
        print(f"{idx}. {link}")

    # Function to fetch and process page content
    def get_page_content(url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            words = text.split()
            content = ""
            for word in words:
                if len(content) + len(word) + 1 > max_chars:
                    break
                content += " " + word
            return content.strip()
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return ""

    # Enrich the search results with body content
    enriched_results = []
    for item in results:
        body = get_page_content(item["link"])
        enriched_results.append(
            {"title": item["title"], "link": item["link"], "snippet": item["snippet"], "body": body}
        )
        time.sleep(1)  # Respect server limits by pausing

    return enriched_results

# Example Usage
if __name__ == "__main__":
    query = "Maggie Tang university of newcastle"
    try:
        print(f"Search Query: {query}\n")
        search_results = google_search(query, num_results=10, max_chars=300)
        print("\nEnriched Results:")
        for idx, result in enumerate(search_results, start=1):
            print(f"\nResult {idx}:")
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}")
            print(f"Body: {result['body']}\n")
    except Exception as e:
        print(f"Error: {e}")
