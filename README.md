*Using the OpenAI SDK with ChatML structured prompts*

`uv add openai` to add openai to the project

Pass `--gemini` to the script to use Gemini instead of OpenAI

```bash
export OPENAI_API_KEY="..." # add your openai api key in the terminal
export GEMINI_API_KEY="..." # add your gemini api key in the terminal
```

Then you should be able to run the app with `uv run main.py`.

If you want to run on a local model, follow 
https://hub.docker.com/r/ollama/ollama and then optionally https://docs.openwebui.com/getting-started/quick-start.
Now you can setup a minimal (5 lines of code) FastAPI server to proxy requests to the local model.

Or use the Transformers library with a Hugging Face model, after installing the library with `uv add transformers torch`.
There is an example usage in `main.py`. Note that this will need quite a bit of disk space and RAM, and ideally you should use a GPU.