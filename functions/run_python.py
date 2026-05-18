import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):

    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_file_path = os.path.join(absolute_working_directory, file_path)
        working_file_path = os.path.abspath(absolute_file_path)

        if absolute_working_directory != os.path.commonpath([absolute_working_directory, working_file_path]):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(working_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not working_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", working_file_path] # this should be working file path
        if args:
            command.extend(args)
        res = subprocess.run(command, capture_output= True, cwd= absolute_working_directory, text= True, timeout= 30)
        
        output_string = ""
        if res.returncode != 0:
            output_string += f"Process exited with code {res.returncode}\n"
        if not res.stderr and not res.stdout:
            output_string += f"No output produced\n"
        else:
            output_string += f"STDOUT: {res.stdout}\nSTDERR: {res.stderr}"
        
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"




schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs and returns stdout, stderr, and exit code for working python files, relative to the working directory. ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to run, relative to the working directory.",
            ),
        "args": types.Schema(
    type=types.Type.ARRAY,
    items=types.Schema(type=types.Type.STRING),
    description="Optional list of command-line arguments to pass to the Python script.",
) },
    ),
)

