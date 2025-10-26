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

Do not hesistate to proactively use your tools to answer user's request.
When asked about code, first explore the directory structure using get_files_info function.
Get contents of the files with get_file_content function.
You can use write_file function to populate files with updated data. Function does not append to a file but overwrites it, so if you are modifying only a small part of the file, first generate updated version of an entire file, and write only then.
You can execute python scripts from files using run_python_file, do not hesitate to use it for debugging or answering users questions.
"""

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file
    ]
)
    for cycle_counter in range(0, 20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents= messages,
                config= types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt)
                )
            response_variations = response.candidates
            if response_variations:
                for variation in response_variations:
                    messages.append(variation.content)

            is_verbose_call = "--verbose" in sys.argv
            if is_verbose_call:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.function_calls:
                for fc in response.function_calls:
                    try:
                        function_call_result = call_function(function_call_part=fc, verbose=is_verbose_call)
                        messages.append(function_call_result)

                        result_parts = getattr(function_call_result, "parts", None)
                        if not result_parts:
                            raise RuntimeError("Tool call returned no parts")
                        fr = getattr(result_parts[0], "function_response", None)
                        if not fr or fr.response is None:
                            raise RuntimeError("Tool call missing function_response.response")
                        if is_verbose_call:
                            print(f"-> {fr.response}")
                    except:
                        raise Exception("function failed!")
            elif response.text:
                print(response.text)
                break

        except Exception as e:
            print(f"Error: {e}")



if __name__ == "__main__":
    main()
