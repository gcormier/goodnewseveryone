import requests
from ollama import chat
from ollama import ChatResponse

def fetchGov(govPrompt):
  BODY_HTML = ""
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
    'content': govPrompt
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
      BODY_HTML += f'<p><a href="{entry.get("link")}">{entry.get("title")}</a> </p>'
      print("-" * 80)
  
  return BODY_HTML
