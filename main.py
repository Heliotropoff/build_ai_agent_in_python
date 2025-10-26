import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python
from functions.write_file import write_file, schema_write_file
from functions.call_functions import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]
    system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file
    ]
)


    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents= messages,
        config= types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
        )

    is_verbose_call = "--verbose" in sys.argv

    if response.function_calls:
        for fc in response.function_calls:
            try:
                function_call_result = call_function(function_call_part=fc, verbose=is_verbose_call)
            except:
                raise Exception("function failed!")
            print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print(response.text)
    if is_verbose_call:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
