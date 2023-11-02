from pydantic import BaseModel, ValidationError
from typing import List, Optional
from fastapi import Form

class Todo(BaseModel):
    id : Optional[int]
    item : str

    @classmethod
    def as_form(
        cls,
        item: str=Form(...)
    ):
        try:
            return cls(item=item)
        except ValidationError as exc:
            print('except error : '+repr(exc.errors()[0]['type']))
            

class TodoItem(BaseModel):
    item:str

    class Config:
        schema_extra = {
            "example":{
                "item":"Read the next chapter of the book"
            }
        }

class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        schema_extra = {
            "example":{
                "todos": [
                    {
                        "item": "Example schema 1!"
                    },
                    {
                        "item": "Example shema 2!"
                    }
                ]
            }
        }