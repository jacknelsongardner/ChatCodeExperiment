from dotenv import load_dotenv
import os
import openai

api_key = "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"
openai.api_key = api_key

prompt = """
I have a system in place to write and delete code files on a hard drive from you. 
The program is running on macOS. 
I need you to not give any comments or anything other than the commands necessary to do whatever you want. 
Your available commands are: NEWFILE : (path of new file) : (text for new file), 
TERMINAL COMMAND : (command you want to enter in terminal)
"""

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=100
)

generated_code = response['choices'][0]['text']
print(generated_code)

working_path: str = os.getcwd()

def create_script(script_name, script_content):
    script_path = os.path.join(working_path, script_name)
    
    with open(script_path, 'w') as script_file:
        script_file.write(script_content)

    return script_path

def get_script_content(script_name):
    script_path = os.path.join(working_path, script_name)

    with open(script_path, 'w') as script_file:
        return script_file.read()

def run_terminal_command(command):
    os.system(command)

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
