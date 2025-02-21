from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Type

# Define Input Schema for Addition
class AddInput(BaseModel):
    """Schema for adding two integers"""
    a: int = Field(..., title="First number", description="This is the first number")
    b: int = Field(..., title="Second number", description="This is the second number")

# Define the Add Tool
class AddTool(BaseTool):
    name: str = "add_tool"
    description: str = "This tool adds two numbers"
    args_schema: Type[BaseModel] = AddInput

    def _run(self, a: int, b: int) -> int:
        """Adds two numbers"""
        return a + b

# Define Input Schema for Multiplication
class MultiplyInput(BaseModel):
    """Schema for multiplying two integers"""
    a: int = Field(..., title="First number", description="This is the first number")
    b: int = Field(..., title="Second number", description="This is the second number")

# Define the Multiply Tool
class MultiplyTool(BaseTool):
    name: str = "multiply_tool"
    description: str = "This tool multiplies two numbers"
    args_schema: Type[BaseModel] = MultiplyInput

    def _run(self, a: int, b: int) -> int:
        """Multiplies two numbers"""
        return a * b

