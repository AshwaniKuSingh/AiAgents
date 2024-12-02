# # pip install tavily-python

# import os
# from dotenv import load_dotenv

# First Example
# Step 1. Instantiating your TavilyClient
from tavily import TavilyClient
tavily_client = TavilyClient(api_key="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")

# Step 2. Executing a simple search query
response = tavily_client.search("Maggie tang from university of newcastle",include_raw_content=True)

# Step 3. That's it! You've done a Tavily Search!
# print(response.keys())
# print(response['query'])
# print(response['follow_up_questions'])
# print(response['answer'])
# print(response['results'][0])
# print()
# print(response['results'][1])
# print()
# print(response['results'][2])
# print()
# print(response['results'][3])
# print()
# print(response['results'][4])
# print(response['response_time'])

# print("Here is the entire content")
# print()
# print(response)



# Access the results with full content
for idx, result in enumerate(response.get('results', []), start=1):
    title = result.get('title')
    url = result.get('url')
    raw_content = result.get('raw_content')  # Full content of the web page
    
    print("=" * 200)  # Separator for clarity
    print(f"Result {idx}")
    print(f"Title: {title}")
    print(f"URL: {url}")
    print(f"Full Content:\n{raw_content}")
    print("=" * 50, "\n")  # Separator marking the end of the result




# Second Example
# from tavily import TavilyClient

# # Step 1. Instantiating your TavilyClient
# tavily_client = TavilyClient(api_key="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")

# # Step 2. Executing a context search query
# context = tavily_client.get_search_context(query="Maggie tang from university of newcastle")

# Step 3. That's it! You now have a context string that you can feed directly into your RAG Application
# # print(context)
# print(type(context))

# import json
# parsed_context = json.loads(context)

# Example 3
# from tavily import TavilyClient

# # Step 1. Instantiating your TavilyClient
# tavily_client = TavilyClient(api_key="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")

# # Step 2. Executing a Q&A search query
# answer = tavily_client.qna_search(query="Maggie tang from university of newcastle")

# # Step 3. That's it! Your question has been answered!
# print(answer)