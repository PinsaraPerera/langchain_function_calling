from pydantic import BaseModel, Field

class Add(BaseModel):
    """add two integers"""

    a: int = Field(..., title="First number", description="This is the first number")
    b: int = Field(..., title="Second number", description="This is the second number")

class Multiply(BaseModel):
    """Multiply two integers"""
    
    a: int = Field(..., title="First number", description="This is the first number")
    b: int = Field(..., title="Second number", description="This is the second number")
