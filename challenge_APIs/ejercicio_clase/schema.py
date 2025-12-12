# schema.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta

class Subtask(BaseModel):
    id: int
    title: str
    completed: bool = False

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    completed: bool = False
    priority: Optional[int] = Field(None, ge=1, le=5, description="Prioridad entre 1 y 5")
    due_date: Optional[datetime] = None
    category: Optional[str] = None
    subtasks: List[Subtask] = []
    
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=1, le=5, description="Prioridad entre 1 y 5")
    due_date: Optional[datetime] = None
    category: Optional[str] = None
    subtasks: Optional[List[Subtask]] = None