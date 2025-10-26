import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    wd_abs = os.path.abspath(working_directory)
    fd_full = os.path.join(working_directory, file_path)
    fd_abs = os.path.abspath(fd_full)
    args = list(args or [])
    #common_path = os.path.commonpath([wd_abs, fd_abs])
    if not fd_abs.startswith(wd_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    path_exists = os.path.exists(fd_abs)
    if not path_exists:
        return f'Error: File "{file_path}" not found.'
    #file_name = file_path
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        arguments = ["python3", file_path, *args]
        completed_process = subprocess.run(
            arguments,
                timeout= 30,
                capture_output=True,
                cwd= wd_abs,
            )
        if completed_process.stdout == b"" and completed_process.stderr == b"":
            result_string = "No output produced."
            return result_string
        out_sting = completed_process.stdout.decode("utf-8")
        err_sting = completed_process.stderr.decode("utf-8")
        #result_string = f'''STDOUT:{out_sting}\nSTDERR: {err_sting}'''
        #result_string = out_sting
        result_string = f'''STDOUT:{out_sting}\nSTDERR: {err_sting}'''
        if completed_process.returncode != 0:
            #result_string = f'''STDOUT:{out_sting}\nSTDERR: {err_sting}'''
            result_string = result_string + f"\nProcess exited with code {completed_process.returncode}"
        return result_string
    except Exception as e:
        return f"Error: executing Python file: {e}"


    # function declaration/schema for the LLM to work with
schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file. The file_path parameter (relative to working directory) specifies which .py file to run. The optional args parameter provides command-line arguments to pass to the script. Returns the script output or an error string.",
    parameters= types.Schema(
        type=types.Type.OBJECT,
        properties= {
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a file that the function will pass to python3 for execution.If file does not exist or does not have .py extension function return an error string."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A python list of strings. Default value is an empty list. Can contain zero or more arguments for a python program."
            )
        }, #required=["file_path"]
    )
)