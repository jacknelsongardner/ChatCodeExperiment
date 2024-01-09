from dotenv import load_dotenv
import os
import subprocess
import tkinter as tk
import re
import multiprocessing

import openai
from openai import OpenAI

# Text Colors
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_WHITE = "\033[97m"

# Command codes
TERMINAL_COMMAND = "TERMINAL COMMAND"
APPROVE_RESULT = "APPROVE"

# Load environment variables from .env
load_dotenv()

# Access the API key from the environment variables
env_key = os.getenv("OPENAI_API_KEY")

# Creating variables to store base and work folders
base_folder = os.getcwd()
work_folder = os.path.join(base_folder,"WORK")

# CHAT FUNCTIONS
def make_chat_request(userprompt: str):
    # Create OpenAI client
    chatclient = openai.OpenAI(api_key=env_key)

    chatprompt = '''
    You are inputting terminal commands into a macOS11 computer. 
    Output each individual command in this format (including brackets): 
    {TERMINAL COMMAND => //command (enters command to terminal)}
    example: TERMINAL COMMAND => (command)\n TERMINAL COMMAND => (second command) etc...always run a terminal commmand at the end to make sure the file you made has expeected code inside and runs as expected"
    '''
    past_messages = [
        {"role": "system", "content": chatprompt},
        {"role": "user", "content": "Create python file in terminal that is blank"},
        {"role": "assistant", "content": '{TERMINAL COMMAND => echo \'print(" ")\' > blankfile.py} \n {TERMINAL COMMAND => python3 blankfile.py}'},
        {"role": "user", "content": userprompt},
    ]
    
    asking = True

    while asking:

        completion = chatclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=past_messages
        )

        chat_output = completion.choices[0].message.content
        
        print(f"\n\n{COLOR_BLUE}CHAT OUTPUT:\n {chat_output}\n\n")
        
        past_response = {"role": "assistant", "content": f"{chat_output}"}
        past_messages.append(past_response)

        chat_commands = parse_commands(chat_output)

        if any(APPROVE_RESULT in command[0] for command in chat_commands):            
            asking = False

        executed_result = execute_commands(chat_commands)
        print(f"{COLOR_GREEN}{executed_result}")

        new_request = {"role": "user", "content": str(executed_result) + "If output is successful as expected, write {APROVE => runs as expected}. Don't forget the brackets or it won't run. If ouput not as expected, write new terminal commands to correct your mistake" }
        past_messages.append(new_request)

    return past_messages

def parse_brackets(response_string):
    # Define a regular expression pattern to match substrings inside curly braces
    pattern = r'\{([^}]+)\}'
    
    # Use re.findall to find all matches in the input string
    matches = re.findall(pattern, response_string)
    
    return matches

def parse_commands(command_string):
    # Parsing commands from brackets as list
    string_commands = parse_brackets(command_string)

    parsed_commands = []

    # 
    for elem in string_commands:

        if elem.startswith(TERMINAL_COMMAND) or elem.startswith(APPROVE_RESULT):
            command = ""
            contents = []
            
            

            parts = elem.split("=>")

            command = parts[0]
            contents = parts[1]

            parsed_commands.append((command,contents))

    return parsed_commands    

def execute_commands(commands_list):
    result = "RESULTS FROM TERMINAL:\n"

    for command_tuple in commands_list:
        
        command_type = command_tuple[0]
        command_content = command_tuple[1]

        if "TERMINAL COMMAND" in command_type:
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
    script_path = os.path.join(work_folder, script_name)

    with open(script_path, 'w') as script_file:
        return script_file.read()

# Runs terminal command and returns output
def run_terminal_command(command):
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=work_folder)
        
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
    
# Main function
def main():

    playing = True
    while playing:
        
        chat_input = input(f"{COLOR_YELLOW}Enter chat request:>> ")

        chat = multiprocessing.Process(target=make_chat_request, args=(chat_input,))
        chat.start()
        chat.join()

if __name__ == "__main__":
    main()
