import os
from google.genai import types
# from functions import config
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    wd_abs = os.path.abspath(working_directory)
    fd_rel = os.path.join(working_directory, file_path)
    fd_abs = os.path.abspath(fd_rel)
    common_abs = os.path.commonpath([wd_abs, fd_abs])
    # print(f"WORKING DIRECTORY: {wd_abs}")
    # print(f"FILE DIRECTORY: {fd_abs}")
    # print(f"COMMON: {common_abs}")
    if wd_abs != common_abs:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    isFile_check = os.path.isfile(fd_abs)
    if not isFile_check:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(fd_abs, "r") as file:
            file_contents_string = file.read(MAX_CHARS + 1)
            if len(file_contents_string) <= MAX_CHARS:
                return file_contents_string
            else:
                trunc_notice = f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                file_contents_string = file_contents_string[:MAX_CHARS] + trunc_notice
            return file_contents_string
    except Exception as e:
        return f"Error: {e}"

    # function declaration/schema for the LLM to work with
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read a specified file, truncates if its longer than 1000 characters and returns a string of file contents or an error string if there was an error. Constrained to the working directory.",
    parameters= types.Schema(
        type=types.Type.OBJECT,
        properties= {
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a file that the function will read and return as a string. Path is relative to the working directory. Not default argumetn. If file_path is not provided or does not point to an existing file, function will return an error"
            ),
        }
    )
)