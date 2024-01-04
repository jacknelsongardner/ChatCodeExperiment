from dotenv import load_dotenv
import os
import subprocess

import multiprocessing

import openai
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Access the API key from the environment variables
env_key = os.getenv("OPENAI_API_KEY")

# CHAT FUNCTIONS
def make_chat_request(userprompt):
    # Create OpenAI client
    chatclient = openai.OpenAI(api_key=env_key)

    chatprompt = """
        Write commands in format below without ANY extra words
        Output ONLY commands, no comments
        Target system : MacOs11
        Comments : No
        Command format example: 
        TERMINAL COMMAND : echo pythonfile.py\n
        TERMINAL COMMAND : python3 pythonfile.py etc..
    """

    completion = chatclient.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[

        {"role": "user", "content": "Create python file in terminal that says hello world when run"},
        {"role": "assistant", "content": 'TERMINAL COMMAND : echo \'print("hello world")\' > helloworldfile.py \n TERMINAL COMMAND : python3 helloworldfile.py'},
        {"role": "user", "content": "Create python file in terminal that adds 2 and 3 when run"},

        ]
    )

    output = completion.choices[0].message
    return str(output.content)

def parse_commands(command_string):
    parsed_commands = []

    for line in command_string.split('\n'):
        if line.startswith('NEWFILE') or line.startswith('OVERWRITE') or line.startswith('TERMINAL COMMAND') or line.startswith('GETOUTPUT') or line.startswith('DONE') or line.startswith('WRITEFILE'):
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

def execute_commands(commands_list):
    result = "RESULTS FROM TERMINAL:\n"

    for command_tuple in commands_list:
        
        command_type = command_tuple[0]
        command_content = command_tuple[1]

        if command_type == "TERMINAL COMMAND": 
            resultadd = run_terminal_command(command_content) 
            result += resultadd

    return result

# CODE MODIFICATION FUNCTIONS
def create_script(script_name, script_content, working_path):
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
            output =  result.stdout.strip()

            return output
        else:
            # Print the error message if the command failed
            return f"Error: {result.stderr}"
    except Exception as e:
        # Handle any exceptions that might occur during the subprocess run
        return f"Exception: {e}"

def insert_code_block(file_path, line_number, code_block):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Insert the code block at the specified line number
    lines.insert(line_number - 1, code_block + '\n')

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

def delete_code_lines(file_path, start_line, end_line):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Delete the specified range of lines
    del lines[start_line - 1:end_line]

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

# PROCESS FUNCTIONS

# Queue commands 
# Format: tuple ( Command type : Sub type : content )
# Example: ( FILECOMM : WRITE : "print(hello world)")

KILL  = 1


# Process queues

backQ = multiprocessing.Queue()
frontQ = multiprocessing.Queue()

# Backend process handling communication with GPT model
def chat_back(fQ):
    if not fQ.empty():
        pass

# Frontend process handling communication with user
def chat_front(bQ):
    if not bQ.empty():
        pass

back_process = multiprocessing.Process(target=chat_back, args=(frontQ,))
front_process = multiprocessing.Process(target=chat_front, args=(backQ,))

# Running processes

def main():
    
    chat_response = make_chat_request("create a python script that says hello world")
    print(chat_response)

    #chat_response = 'TERMINAL COMMAND : echo \'print("hello world")\' > filename111.py \nTERMINAL COMMAND : python3 filename111.py'
    chat_commands = parse_commands(chat_response)
    print(chat_commands)

    execute_result = execute_commands(chat_commands)
    print(execute_result)

if __name__ == "__main__":
    main()
