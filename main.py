import json
import os
from src.tools import tools, AddTool, MultiplyTool, CreateToDoTool, RemoveToDoTool, GetToDoTool
from src.config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from src.db.base import Base
from src.db.session import engine

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize LLM
MODELS = ["gpt-3.5-turbo", "gpt-4o-mini"]
llm = ChatOpenAI(model=MODELS[0], temperature=0, api_key=OPENAI_API_KEY)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools, strict=True)

# Token tracking file
TOKEN_FILE = "tokens.json"

if __name__ == "__main__":
    while True:
        user_input = input("Enter your input: ")
        if user_input.lower() == "exit":
            break

        messages = [HumanMessage(user_input)]
        ai_response = llm_with_tools.invoke(messages)
        messages.append(ai_response)

        # Process tool calls
        tool_mapping = {"add_tool": AddTool(), "multiply_tool": MultiplyTool(), "create_todo": CreateToDoTool(),
                        "get_todo": GetToDoTool(), "remove_todo": RemoveToDoTool()}

        for tool_call in ai_response.tool_calls:
            selected_tool = tool_mapping.get(tool_call["name"])
            if selected_tool:
                tool_output = selected_tool.invoke(tool_call["args"])
                messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

        # Get final LLM response
        response = llm_with_tools.invoke(messages)

        # Read token data
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                try:
                    token_data = json.load(f)
                except json.JSONDecodeError:
                    token_data = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}
        else:
            token_data = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}

        # Update token usage
        token_usage = response.response_metadata.get("token_usage", {})
        token_data["completion_tokens"] += token_usage.get("completion_tokens", 0)
        token_data["prompt_tokens"] += token_usage.get("prompt_tokens", 0)
        token_data["total_tokens"] += token_usage.get("total_tokens", 0)

        # Save token usage
        with open(TOKEN_FILE, "w") as f:
            json.dump(token_data, f, indent=4)

        print(response.content)
