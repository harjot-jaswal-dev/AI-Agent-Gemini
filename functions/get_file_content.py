import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    
    try: 
        working_absolut_path = os.path.abspath(working_directory)
        file_path_absolute = os.path.abspath(file_path)

        if not os.path.commonpath([working_absolut_path, file_path_absolute]):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_absolute):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        

        with open(file_path_absolute) as f:
            contents = f.read(1000)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'


    except Exception as e:
        return f"Error: {e}"