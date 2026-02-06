# Using the OpenAI SDK with ChatML structured prompts and the OpenAI Agents SDK

## Running with frontier models
Pass `--gemini` to the script to use Gemini instead of OpenAI, although not all functionality transfers over as-is.

```bash
export OPENAI_API_KEY="..." # add your openai api key in the terminal
export GEMINI_API_KEY="..." # add your gemini api key in the terminal (optionally)
```

Then you should be able to run the app with `uv run main.py`. 

## Agent Builder
OpenAI has a GUI tool for visually putting together entire agentic flows. You can export the results and refine them in python or typescript.

## Local models
Follow https://hub.docker.com/r/ollama/ollama and then optionally https://docs.openwebui.com/getting-started/quick-start.
Now you can setup a minimal (5 lines of code) FastAPI server to proxy requests to the local model.

Or use the Transformers library with a Hugging Face model, which is demonstrated in this repo but code is commented out for that
since it needs quite a bit of disk space and RAM, and ideally you should use a GPU rather than CPU which was configured in the `pyproject.toml`.

## MCP servers
The `python_mcp` folder in this project is not openai related, it just shows how to write an MCP server in python.

The Agent SDK does allow you to talk to MCP tools, an example for that is in `mcp_with_openai_agent.py`. 

## RAG as a tool
OpenAI's built-in vector store is [called File Search](https://openai.github.io/openai-agents-python/ref/tool/#agents.tool.FileSearchTool).
In Agent Builder, you can drop a text file to the workflow and it will be converted to a vector store.
