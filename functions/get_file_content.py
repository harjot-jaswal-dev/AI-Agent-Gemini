import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    
    try: 
        working_absolut_path = os.path.abspath(working_directory)
        file_path_join = os.path.join(working_directory, file_path)
        working_file_path = os.path.abspath(file_path_join)

        if working_absolut_path !=  os.path.commonpath([working_absolut_path, working_file_path]):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(working_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        

        with open(working_file_path) as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return contents

    except Exception as e:
        return f"Error: {e}"