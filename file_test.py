import os

def list_contents(directory, indent=0):
    try:
        # Check if the provided path is a directory
        if os.path.isdir(directory):
            contents = os.listdir(directory)
            output = ""

            for item in contents:
                item_path = os.path.join(directory, item)
                prefix = "    " * indent

                if os.path.isdir(item_path):
                    output += f"{prefix}[Folder] {item}\n"
                    output += list_contents(item_path, indent + 1)
                else:
                    output += f"{prefix}[File] {item}\n"

            return output
        else:
            return f"Error: The provided path is not a directory."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage:
base_dir = os.getcwd()
work_dir = os.path.join(base_dir,"WORK")
result = list_contents(work_dir)

print(f"Contents of {work_dir}:\n{result}")
