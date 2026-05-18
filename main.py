import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key was empty")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="user_prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):

        response = client.models.generate_content(model= "gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions] ,system_instruction=system_prompt))

        if response.candidates:
            for i in response.candidates:
                messages.append(i.content)

        if response.usage_metadata is None:
            raise RuntimeError("usage_metadata was None")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if response.function_calls:
            function_responses = []
            for f in response.function_calls:
                function_call_results = call_function(f, verbose= args.verbose)
                if not function_call_results.parts:
                    raise Exception("function_call_result has no parts")
                if function_call_results.parts[0].function_response is None:
                    raise Exception("function_response is None")
                if function_call_results.parts[0].function_response.response is None:
                    raise Exception("response is None")
                if args.verbose:
                    print(f"-> {function_call_results.parts[0].function_response.response}")

                function_responses.append(function_call_results.parts[0])

            messages.append(types.Content(role="user", parts=function_responses))

        else:
            print(f"Response:\n{response.text}")
            break
    
    else:
        print("Maximum iterations reached without a final response")
        exit(1)

if __name__ == "__main__":
    main()
