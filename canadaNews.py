import requests
import json
from ollama import chat
from ollama import ChatResponse
import feedparser

rss_url = "https://www.cbc.ca/webfeed/rss/rss-topstories"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
feed = feedparser.parse(rss_url, request_headers=headers)


# Extract and display items from the feed
rss_items = []


for entry in feed.entries:
  item = {
      "title": entry.title,
      "link": entry.link,
      "description": entry.description,
      "pubDate": entry.published,
      "category": getattr(entry, "category", "No category available")
  }
  
  rss_items.append(item)


# Loop through rss_items and print each item
for item in rss_items:
  response: ChatResponse = chat(model='llama3.2', messages=[
  {
  'role': 'system',
  'content': 'Your only purpose is to view news headlines and summaries. If there is any HTML looking content, you can ignore it and only use the text found within.\
              Your only response will be a 1 or 0 zero, which is to represent true or false. A true response indicates positive or interesting news, and a false response indicates news that is not of interest. \
              You are to return a 0 if the news is about war, conflict, donald trump, or any other negative news. This could be a disaster, a fire, crime, murder. It might also be related to financial woes, bad economy, poor living conditions. Anything involving a fatality is bad news.\
              Technology and science news is positive news. An example would be a cyber attack or hacking attempt, these should be a positive response.\
              If you are uncertain, you can return a 1. You will be provided the full text in a subsequent message for evaluation.',
  },
  {
    'role': 'user',
    'content': f'Your headline is {item["title"]}, and the description is {item["description"]}.',
  },
  ])
  
  if response.message.content == '1':
    print(f"Title: {item['title']}")
    print(f"Link: {item['link']}")
    #print(f"Description: {item['description']}")
    print("-" * 80)
