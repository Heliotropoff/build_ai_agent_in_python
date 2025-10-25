import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    full_absolute = os.path.abspath(full_path)
    working_directory_absolute = os.path.abspath(working_directory)
    #directory_absolute = os.path.abspath(directory)

    common_wd_full = os.path.commonpath([working_directory_absolute,full_absolute])

    if working_directory_absolute != common_wd_full:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_absolute):
        return f'Error: "{full_absolute}" is not a directory'

    try:
        files_list = os.listdir(full_absolute)
    except Exception as e:
        return f"Error:{e}"

    desc_string = ""
    for file in files_list:
        try:
            file_dir = os.path.abspath(os.path.join(full_absolute, file))
            dir_check_file = os.path.isdir(file_dir)
            size = os.path.getsize(file_dir)
        except Exception as e:
            return f"Error: {e}"

        desc_string += f"- {file}: file_size={size} bytes, is_dir={dir_check_file} \n"
    return desc_string
