import requests
import json
from ollama import chat
from ollama import ChatResponse


# Define the API endpoint
url = "https://api.io.canada.ca/io-server/gc/news/en/v2"
params = {
    "sort": "publishedDate",
    "orderBy": "desc",
    "publishedDate>": "2024-11-01",
    "pick": 200
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Loop through each item in the JSON and print details
entries = data.get("feed", {}).get("entry", [])
for entry in entries:
    response: ChatResponse = chat(model='llama3.2', options={"temperature" : 0.1}, messages=[
    {
    'role': 'system',
    'content': 'Your only purpose is to view news headlines and summaries. \
                You will be looking at headlines that are published by the Government of Canada. \
                Your only response will be a 1 or 0 zero, which is to represent true or false. \
                You are to return 0, unless news relates to any of the following : \
                Fisheries and Oceans Canada, US Coast Guard, fisheries, the fishing industry, \
                the oceans as it relates to conservation and climate change, climate change, illegal fishing, \
                illegal poaching, the Canadian Coast Guard. \
                Finally you can also return a 1 if the headline relates to changes in government structure that might affect or relate to that list',
  },
  {
    'role': 'user',
    'content': f'Your headline is {entry.get("title")}, and the summary is {entry.get("teaser")}.',
  },

])

    if response.message.content == '1':
        print("Relevant news found:")
        print(f"Title: {entry.get('title')}")
        print(f"Published Date: {entry.get('publishedDate')}")
        print(f"Teaser: {entry.get('teaser')}")
        print(f"Link: {entry.get('link')}")
        print("-" * 80)
