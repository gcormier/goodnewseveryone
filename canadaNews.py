from ollama import chat
from ollama import ChatResponse
import feedparser
from dotenv import load_dotenv
import os
from gregEmail import send_email


rss_url = "https://www.cbc.ca/webfeed/rss/rss-topstories"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
feed = feedparser.parse(rss_url, request_headers=headers)

def fetchCan(canPrompt):
  BODY_HTML = ""
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
    response: ChatResponse = chat(model='llama3.2', options={"temperature" : 0.1}, messages=[
    {
    'role': 'system',
    'content': canPrompt,
    },
    {
      'role': 'user',
      'content': f'Your headline is {item["title"]}, and the description is {item["description"]}.',
    },
    ])
    
    if response.message.content == '1':
      BODY_HTML += f'<p><a href="{item['link']}">{item['title']}</a> </p>'
      print(f"Title: {item['title']}")
      print(f"Link: {item['link']}")
      #print(f"Description: {item['description']}")
      print("-" * 80)

  return BODY_HTML


