from dotenv import load_dotenv
import os

import openai
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Access the API key from the environment variables
env_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
chatclient = openai.OpenAI(api_key=env_key)

chatprompt = """
Write no extra words
Target system : MacOs11
Commands: 
1. WRITEFILE : (path) : (text)
2. TERMINAL COMMAND : (command)
"""

userprompt = "Write and run a script that prints Hello World"

completion = chatclient.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": chatprompt},
    {"role": "user", "content": userprompt}
  ]
)

generated_code = completion.choices[0].message
print(generated_code)