import argparse
import os
import json
from openai import OpenAI
from transformers import pipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gemini", action="store_true", help="Use Gemini via OpenAI-compatible API")
    args = parser.parse_args()

    # Using Transformers library with a Hugging Face model
    pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
                {"type": "text", "text": "What animal is on the candy?"}
            ]
        },
    ]
    pipe(text=messages)    
    
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
    # CoT improves the answer quality by making the AI think step by step; example:
    message_history = [
        { "role": "system", "content": """
            You are an enlightened master of Tibetan wisdom. You are answering questions using chain of thought reasoning.
            You work on START, THINK, and END steps. THINK can be multiple steps, looking at the question from multiple perspectives.
            Once THINK is done, you move to END.

            Rules:
            - Stricly follow the given JSON format in your response
            - Only run one steps at a time
            
            Output format:
            {
                "step": "START" | "THINK" | "END",
                "content": "content"
            }
            """ }
    ]
    initial_query = { "role": "user", "content": "What is the meaning of life?" }
    message_history.append(initial_query)
    while True:
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=message_history
        )
        raw_result = response.choices[0].message.content
        response_content = json.loads(raw_result)
        message_history.append({ "role": "assistant", "content": raw_result })
        if response_content.get("step") == "END":
            print(f"{prefix} {response_content}")
            break

if __name__ == "__main__":
    main()
