from .math_tools import AddTool, MultiplyTool
from .db_tool import CreateToDoTool, RemoveToDoTool, UpdateToDoTool, GetToDoTool

tools = [AddTool(), MultiplyTool(), CreateToDoTool(), RemoveToDoTool(), GetToDoTool()]