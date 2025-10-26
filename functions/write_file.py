import os
from google.genai import types

def write_file(working_directory, file_path, content):
    fd = os.path.join(working_directory, file_path)
    wd_abs = os.path.abspath(working_directory)
    fd_abs = os.path.abspath(fd)
    common_path = os.path.commonpath([wd_abs, fd_abs])
    if wd_abs != common_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    fileExists = os.path.exists(fd_abs)
    if not fileExists:
        try:
            path2file = os.path.dirname(fd_abs)
            os.makedirs(path2file, exist_ok=True)
        except Exception as e:
            return f"Error: {e}"
    try:
        with open(fd_abs, "w") as file:
            file.write(content)
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


# function declaration/schema for the LLM to work with
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Receives file_path and contents strings. File_path is relative to working directory. If file_path leads to an existing file it opens this file and writes it over with contents. If file does not exists, it creates the file and writes in the contes. Returns a string with information how many character were written to which file or returns an error if something happend during the writing process.",
    parameters= types.Schema(
        type=types.Type.OBJECT,
        properties= {
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a file that the function will write contents to. Path is relative to the working directory. If file_path leads to an existing file it opens this file and writes it over with contents. If file does not exists, it creates the file and writes in the contes."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string that contains a contents that caller wants to write into the file"
            )
        }
    )
)