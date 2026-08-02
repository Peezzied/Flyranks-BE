from pydantic import BaseModel

class Item(BaseModel):
    title: str | None = None
    done: bool | None = None