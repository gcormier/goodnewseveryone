from govNews import *
from canadaNews import *
from ollama import chat
from ollama import ChatResponse
from dotenv import load_dotenv
import os
from gregEmail import send_email

ses_user = os.getenv("SES_USER")
ses_key = os.getenv("SES_KEY")

destEmail = "gcormier@gmail.com"

govPrompt = """
You will be looking at headlines that are published by the Government of Canada.
Your only response will be a 1 or 0.
You are to return 0, unless news relates to any of the following :
Fisheries and Oceans Canada, US Coast Guard, fisheries, the fishing industry,
the oceans as it relates to conservation and climate change, climate change, illegal fishing,
illegal poaching, the Canadian Coast Guard.
You can also return a 1 if the headline relates to changes in government structure that might affect, have impact or relate to the list above.
"""

canPrompt = """
Your only purpose is to view news headlines and summaries. If there is any HTML looking content, you can ignore it and only use the text found within.
Your only response will be a 1 or 0. A response of 1 indicates news I want to see, and a response of 0 indicates news that I do not want to see.
News I don't want to see includes news is about war, conflict, donald trump, or any other news that could be seen as negative or depressing. 
Examples of this kind of news might include a disaster, a fire, crime, murder, terrorism, threats, slander, financial woes, bad economy, poor living conditions, or anything else related to murder, crime, terrorism, bombings or disasters.
The only exception to this is cyber crime, cyber warfare or hacking, whether it is successful or not.
I want to see news about science and technology. Other positive news stories are things I want to see as well. I'm also interested in computers, manufacturing, nature, the envrionment and travel.
"""
govNews = ""
canNews = ""
govNews = fetchGov(govPrompt)
canNews = fetchCan(canPrompt)

response: ChatResponse = chat(model='llama3.2', options={"temperature" : 0.8}, messages=[
{
'role': 'user',
'content': 'Generate a friendly and positive inspirational quote of the day. You can quote a famous quote, or create a new positive message. Provide me the inspirational quote only that you generate, do not preface it or conclude it with anything.'
},])

BODY_HTML = f"""
<h1>Good news everyone!</h1>
<h3>{response.message["content"]}</h3>
<h2>GoC</h2>
{govNews}
<hr>
<h2>In the world</h2>
{canNews}

<br><br>
<hr>
<span style="font-size: smaller; color: #808080;">
Gov Prompt:<br>
{govPrompt}<br><br>

Can Prompt:<br>
{canPrompt}<br><br>
</span>'
"""
send_email(destEmail, BODY_HTML, ses_user, ses_key)

