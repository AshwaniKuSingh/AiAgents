import os
import requests
from dotenv import load_dotenv

def google_search_links(query: str, num_results: int = 5) -> list:
    """
    Perform a Google search and return only the links for the results.
    
    :param query: Search query string.
    :param num_results: Number of results to fetch (default: 5).
    :return: List of links.
    """
    # Load API credentials from the .env file
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    if not api_key or not search_engine_id:
        raise ValueError("API key or Search Engine ID not found in environment variables")

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": search_engine_id, "q": query, "num": num_results}

    # Perform the API request
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error in API request: {response.status_code}")

    # Parse the results
    results = response.json().get("items", [])
    links = [item["link"] for item in results]  # Extract links only

    return links

# Example Usage
if __name__ == "__main__":
    # Replace with your search query
    query = "Maggie Tang"
    try:
        print(f"Search Query: {query}\n")
        links = google_search_links(query, num_results=5)
        print("Search Results:")
        for idx, link in enumerate(links, start=1):
            print(f"{idx}. {link}")
    except Exception as e:
        print(f"Error: {e}")
