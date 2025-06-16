from enum import IntEnum
from typing import List, Optional
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field

api = FastAPI()

class Priority(IntEnum):
    LOW=3
    MEDIUM=2
    HIGH=1

class TodoBase(BaseModel):
    todo_item: str = Field(..., min_length = 3, max_length=512, description='Name of the task')
    todo_task: str = Field(...,description='Dsecription of the todo')
    priority: Priority = Field(default=Priority.LOW,description='Priority of todo')

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(...,description='Unique ID for Todo')

#TodoUpdate can not have TodoBase Model because in a single update call thare can be update for only one field, so other fields are not required means they are optional. So for different structure we need to inherit BaseModel not TodoBase. Like creating a new TodoBase Model structure.
class TodoUpdate(BaseModel):
    todo_item: Optional[str] = Field(None, min_length = 3, max_length=512, description='Name of the task')
    todo_task: Optional[str] = Field(None,description='Dsecription of the todo')
    priority: Optional[Priority] = Field(None,description='Priority of todo')


allTodos=[
    Todo(todo_id=1, todo_item="sports", todo_task="Go to Gym",priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_item="study", todo_task="Study to crack Microsoft",priority=Priority.HIGH),
    Todo(todo_id=3, todo_item="read", todo_task="Read 10 Pages Daily",priority=Priority.MEDIUM),
    Todo(todo_id=4, todo_item="meditate", todo_task="Go to Gym",priority=Priority.MEDIUM),
    Todo(todo_id=5, todo_item="shop", todo_task="Go shopping",priority=Priority.LOW)
]


#path parameters using /
@api.get('/todo/{todo_id}',response_model=Todo)
def getTodo(todo_id: int):
    for todo in allTodos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail='Todo Not Found')

#query Parameters using ?
@api.get('/todos',response_model=List[Todo])
def getAllTodos(firstN: int = None):
    if firstN:
        return allTodos[:firstN]
    else:
        return allTodos
    
@api.post('/todos',response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id=max(todo.todo_id for todo in allTodos) + 1
    new_todo = Todo(todo_id=new_todo_id, 
                todo_item=todo.todo_item, 
                todo_task=todo.todo_task,
                priority=todo.priority)
    allTodos.append(new_todo)
    return new_todo

@api.put('/todos',response_model=Todo)
def update_todo(todo_id:int, updated_todo:TodoUpdate):
    for todo in allTodos:
        if todo.todo_id == todo_id:
            if updated_todo.todo_item is not None:
                todo.todo_item = updated_todo.todo_item
            if updated_todo.todo_task is not None:
                todo.todo_task = updated_todo.todo_task
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
    raise HTTPException(status_code=404, detail='Todo Not Found')

@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    for index,todo in enumerate(allTodos):
        if todo.todo_id == todo_id:
            deleted_todo=allTodos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail='Todo Not Found')