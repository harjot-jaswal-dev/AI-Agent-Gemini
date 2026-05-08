import os

def write_file(working_directory, file_path, content):

    try:
        working_absolute_path = os.path.abspath(working_directory)
        file_path_join = os.path.join(working_directory, file_path)
        file_path_absolute = os.path.abspath(file_path_join)

        if working_absolute_path !=  os.path.commonpath([working_absolute_path, file_path_absolute]):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_path_absolute):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_dir = os.path.dirname(file_path_absolute)
        os.makedirs(parent_dir, exist_ok=True)

        with open(file_path_absolute, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"