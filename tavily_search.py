# pip install tavily-python

import os
from dotenv import load_dotenv

from tavily import TavilyClient


# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key="")

# Step 2. Executing a simple search query
response = tavily_client.search("Who is Leo Messi?")

# Step 3. That's it! You've done a Tavily Search!
print(response)


