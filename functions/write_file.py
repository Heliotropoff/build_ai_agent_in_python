import os

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