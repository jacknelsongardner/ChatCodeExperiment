from dotenv import load_dotenv
import os
import subprocess


import openai
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Access the API key from the environment variables
env_key = os.getenv("OPENAI_API_KEY")


def make_chat_request():
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
    

def create_script(script_name, script_content):
    script_path = os.path.join(working_path, script_name)
    
    with open(script_path, 'w') as script_file:
        script_file.write(script_content)

    return script_path

def get_script_content(script_name):
    script_path = os.path.join(working_path, script_name)

    with open(script_path, 'w') as script_file:
        return script_file.read()

# Runs terminal command and returns output
def run_terminal_command(command):
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        # Check if the command was successful (return code 0)
        if result.returncode == 0:
            # Return the captured output
            return result.stdout.strip()
        else:
            # Print the error message if the command failed
            return f"Error: {result.stderr}"
    except Exception as e:
        # Handle any exceptions that might occur during the subprocess run
        return f"Exception: {e}"

def parse_commands(commands):
    parsed_commands = []

    for line in commands.split('\n'):
        if line.startswith('NEWFILE') or line.startswith('OVERWRITE') or line.startswith('TERMINAL COMMAND') or line.startswith('GETOUTPUT') or line.startswith('DONE'):
            command = ""
            contents = []
            parts = line.split(" : ")

            if len(parts) > 0:
                command = parts[0]
                del parts[0]
            
            if len(parts) > 0:
                contents = parts

            parsed_commands.append((command,contents))

    return parsed_commands



def test():
    # Define the script content (you can modify this as needed)
    script_content = """
print("Hello, this is a dynamically created Python script!")
print("You can add your own logic here.")
    """

    # Create and run the script in the current working directory
    script_name = 'dynamic_script.py'
    script_path = create_script(script_name, script_content)
    run_terminal_command(f"python3 ")

if __name__ == "__main__":
    test()
