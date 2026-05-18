import os
from google.genai import types


def get_files_info(working_directory, directory="."):

    working_absolute_path = os.path.abspath(working_directory)

    join_path = os.path.join(working_absolute_path, directory)

    target_dir = os.path.normpath(join_path)

    valid_target_dire = os.path.commonpath([working_absolute_path, target_dir])

    if valid_target_dire != working_absolute_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    

    try:
        contents_list = os.listdir(target_dir)
        res_string = []
        for content in contents_list:
            file_path = os.path.join(target_dir, content)
            curr = f" - {content}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
            res_string.append(curr)
        return "\n".join(res_string)
    except Exception as e:
        return f"Error: {e}"
    


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)