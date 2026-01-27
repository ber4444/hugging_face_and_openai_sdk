import argparse
import os
import json
import platform
from openai import OpenAI
from transformers import pipeline
from pydantic import BaseModel, Field
from typing import Optional

def get_platform():
    return platform.system()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gemini", action="store_true", help="Use Gemini via OpenAI-compatible API")
    args = parser.parse_args()

    # Using Transformers library with a Hugging Face model
    """ pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
                {"type": "text", "text": "What animal is on the candy?"}
            ]
        },
    ]
    pipe(text=messages)    """ 
    
    if args.gemini:
        # Use Gemini via OpenAI-compatible API
        # There is also a google-genai package that could be used for Gemini instead of the OpenAI SDK
        client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/"
        )
        model = "gemini-2.0-flash"
        prefix = "Gemini (OpenAI SDK):"
    else:
        # standard OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = "gpt-4o-mini"
        prefix = "OpenAI:"

    response = client.chat.completions.create(
        model=model,
        messages=[
            # you should always start with a system message that sets the context/role of the AI
            # define here the format of the response too
            # you should also include 50-60 examples to increase the quality of the AI's responses by 50x
            { "role": "system", "content": """
            You are an expert in Math. Only respond to Math questions.

            Rule:
            - Stricly follow the JSON format in your response

            Output format:
            {
                "decimal": "decimal answer",
                "binary": "binary answer"
            }
            
            Examples:
            Q: What is 2+2?
            A: {"decimal": "4", "binary": "10"}
            """ },
            { "role": "user", "content": "What is 3+3?" }
        ]
    )
    print(f"{prefix} {response.choices[0].message.content}")

    # CoT improves the answer quality by making the AI think step by step; example that also shows tool calling:
    available_tools = { "get_platform": get_platform }
    message_history = [
        { "role": "system", "content": """
            You are answering questions using chain of thought reasoning.
            You work on START, PLAN, and END steps. PLAN can be multiple steps.
            Once PLAN is done, you move to END.
            You can also call a tool from the list of available tools.
            For every tool call, wait for the observe step which is the output of the called tool.

            Rules:
            - Stricly follow the given JSON format in your response
            - Only run one step at a time
            - The sequence of steps if START, PLAN and END

            Available tools:
            - get_platform(): return the name of the current platform
            
            Output format:
            {
                "step": "START" | "PLAN" | "END" | "TOOL" | "OBSERVE",
                "content": "string", "tool": "string"
            }

            Examples:
            START: What is my current OS?
            PLAN: { "step": "PLAN", "content": "Seems like user is interested in the name of his current platform" }
            PLAN: { "step": "PLAN", "content": "I see get_platform() in the available tools, let's call that to get the platform" }
            PLAN: { "step": "TOOL", "tool": "get_platform" }
            PLAN: { "step": "OBSERVE", "tool": "get_platform", "output": "Linux" }
            PLAN: { "step": "PLAN", "content": "Great, I got the current OS." }
            END:  { "step": "END", "content": "The current OS is Linux" }
            """ }
    ]
    class MyOutputFormat(BaseModel):
        step: str = Field(..., description="The ID of the step, such as PLAN or TOOL") 
        content: Optional[str] = Field(None, description="The optional content of the step")
        tool: Optional[str] = Field(None, description="The ID of the tool call")
    initial_query = { "role": "user", "content": "How do I run a python file on my OS?" }
    message_history.append(initial_query)
    while True:
        response = client.chat.completions.parse(
            model=model,
            response_format=MyOutputFormat,
            messages=message_history
        )
        response_content = response.choices[0].message.parsed
        message_history.append({ "role": "assistant", "content": response.choices[0].message.content })
        if response_content.step == "TOOL":
            tool_to_call = response_content.tool
            tool_response = available_tools[tool_to_call]()
            print(f"tool gave: {tool_response}")
            message_history.append({ "role": "developer", "content": json.dumps(
                { "step": "OBSERVE", "tool": tool_to_call, "output": tool_response } 
            ) })
            continue
        if response_content.step == "END":
            print(f"{prefix} {response_content}")
            break

if __name__ == "__main__":
    main()
