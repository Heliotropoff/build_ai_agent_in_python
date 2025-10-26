from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python
from functions.write_file import write_file, schema_write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    wd = "./calculator"
    function_name = function_call_part.name
    funcs = {
        "get_files_info":get_files_info,
        "get_file_content": get_file_content,
        "write_file":write_file,
        "run_python_file":run_python_file,
    }
    kwargs = dict(function_call_part.args or {})
    kwargs["working_directory"] = wd
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    if function_name not in funcs:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                    )
                    ],
                    )
    function_result = funcs[function_name](**kwargs)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)
