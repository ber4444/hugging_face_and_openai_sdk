# Using the OpenAI SDK with ChatML structured prompts and the OpenAI Agents SDK

## Running with frontier models
Pass `--gemini` to the script to use Gemini instead of OpenAI, although not all functionality transfers over as-is.

```bash
export OPENAI_API_KEY="..." # add your openai api key in the terminal
export GEMINI_API_KEY="..." # add your gemini api key in the terminal (optionally)
```

Then you should be able to run the app with `uv run main.py`. There is also an MCP example in `mcp_with_openai_agent.py`. 

`python_mcp` is not openai related, it just shows how to write an MCP server in python.

## Local models
Follow https://hub.docker.com/r/ollama/ollama and then optionally https://docs.openwebui.com/getting-started/quick-start.
Now you can setup a minimal (5 lines of code) FastAPI server to proxy requests to the local model.

Or use the Transformers library with a Hugging Face model, which is demonstrated in this repo but code is commented out for that
since it needs quite a bit of disk space and RAM, and ideally you should use a GPU rather than CPU which was configured in the `pyproject.toml`.

## LangGraph, LangChain

While the OpenAI Agent SDK does allow agents to maintain conversation history without manual memory management, it doesn't support checkpointing, so if you re-run the app, conversation history is lost. You can use LangGraph, MS Agent Framework or similar and a DB to implement that.

There is also no RAG support but you can combine the Agent SDK with a LangChain RAG. Or, if your files are already structured in a database, you do not even need a RAG and can use an MCP which is supported by the Agents SDK.

## Agents and AGI
Fully autonomous agents are a step towards AGI but today's LLMs are pure next-token predictors. 
They may serve the basis for AGI once they move to being embodied, long term learners, etc.

