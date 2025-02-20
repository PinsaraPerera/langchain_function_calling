import json
from src.models.Math_models import Add, Multiply
from src.config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from src.tools.math_tools import add, multiply

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

# Define tools
tools = [add, multiply]

# Bind tools
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

        for tool_call in ai_response.tool_calls:
            selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
            tool_output = selected_tool.invoke(tool_call["args"])
            messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

        response = llm_with_tools.invoke(messages)

        # Read existing token data
        try:
            with open(TOKEN_FILE, "r") as f:
                token_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            token_data = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}

        # Update token usage
        token_usage = response.response_metadata["token_usage"]
        token_data["completion_tokens"] += token_usage.get("completion_tokens", 0)
        token_data["prompt_tokens"] += token_usage.get("prompt_tokens", 0)
        token_data["total_tokens"] += token_usage.get("total_tokens", 0)

        # Write updated token data
        with open(TOKEN_FILE, "w") as f:
            json.dump(token_data, f, indent=4)

        print(response.content)
