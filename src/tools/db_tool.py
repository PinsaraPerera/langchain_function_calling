from src.db.session import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict
from langchain_core.tools import BaseTool
from src.models.ToDoModel import TodoModel
from typing import Type, List, Dict, Optional
from datetime import datetime

# Define Input schema for create_todo
class CreateToDoInput(BaseModel):
    title: str = Field(..., title="Title of the todo", description="This is the title of the todo")
    description: str = Field(..., title="Description of the todo", description="This is the description of the todo")
    due_date: str = Field(..., title="Due date of the todo", description="Due date (YYYY-MM-DD) of the todo")

# Define the CreateToDo Tool
class CreateToDoTool(BaseTool):
    name: str = "create_todo"
    description: str = "This tool creates a new todo"
    args_schema: Type[BaseModel] = CreateToDoInput

    def _run(self, title: str, description: str, due_date: str) -> str:
        """Creates a new todo"""
        db: Session = SessionLocal()
        try:
            new_todo = TodoModel(title=title, description=description, due_date=due_date)
            db.add(new_todo)
            db.commit()
            return f"Todo '{title}' created successfully"
        except Exception as e:
            db.rollback()
            return f"Error creating todo: {str(e)}"
        finally:
            db.close()

# Define the input schema for get_all_todo
class GetToDoInput(BaseModel):
    id: str = Field(..., title="ID of the todo", description="This is the ID of the todo")

# Define the GetToDoTool
class GetToDoTool(BaseTool):
    name: str = "get_todo"
    description: str = "This tool gets a todo"
    args_schema: Type[BaseModel] = GetToDoInput

    def _run(self, id: str) -> Dict[str, str]:
        """Gets a todo"""
        db: Session = SessionLocal()
        try:
            todo = db.query(TodoModel).filter(TodoModel.id == int(id)).first()
            if todo:
                return {"title": todo.title, "description": todo.description, "due_date": todo.due_date}
            return {"error": "Todo not found"}
        except Exception as e:
            return {"error": f"Error getting todo: {str(e)}"}
        finally:
            db.close()

# Define RemoveToDoInput schema
class RemoveToDoInput(BaseModel):
    id: str = Field(..., title="ID of the todo", description="This is the ID of the todo")

# Define the RemoveToDoTool
class RemoveToDoTool(BaseTool):
    name: str = "remove_todo"
    description: str = "This tool removes a todo"
    args_schema: Type[BaseModel] = RemoveToDoInput

    def _run(self, id: str) -> str:
        """Removes a todo"""
        db: Session = SessionLocal()
        try:
            todo = db.query(TodoModel).filter(TodoModel.id == int(id)).first()
            if todo:
                db.delete(todo)
                db.commit()
                return "Todo removed successfully"
            return "Todo not found"
        except Exception as e:
            db.rollback()
            return f"Error removing todo: {str(e)}"
        finally:
            db.close()

# Define UpdateToDoInput schema
class UpdateToDoInput(BaseModel):
    id: int = Field(..., title="ID of the todo", description="This is the ID of the todo")
    title: Optional[str] = Field(None, title="Title of the todo", description="This is the title of the todo")
    description: Optional[str] = Field(None, title="Description of the todo", description="This is the description of the todo")

# Define the UpdateToDoTool
class UpdateToDoTool(BaseTool):
    name: str = "update_todo"
    description: str = "This tool updates a todo"
    args_schema: Type[BaseModel] = UpdateToDoInput

    def _run(self, id: int, title: Optional[str] = None, description: Optional[str] = None) -> str:
        """Updates a todo"""
        db: Session = SessionLocal()
        try:
            todo = db.query(TodoModel).filter(TodoModel.id == id).first()
            if todo:
                if title:
                    todo.title = title
                if description:
                    todo.description = description
                db.commit()
                return "Todo updated successfully"
            return "Todo not found"
        except Exception as e:
            db.rollback()
            return f"Error updating todo: {str(e)}"
        finally:
            db.close()
