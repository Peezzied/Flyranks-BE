from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, model_validator, ValidationError
import json

TASKS = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Walk the dog", "done": True},
    {"id": 3, "title": "Read a book", "done": False},
]


class Item(BaseModel):
    title: str | None = None
    done: bool | None = None


app = FastAPI()


@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(item: Item):
    title = item.title
    if title is None or not isinstance(title, str) or not title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="title is required and cannot be empty",
        )

    title_str = title.strip()

    new_id = (
        1 if len(TASKS) == 0 else max(t["id"] for t in TASKS) + 1
    )  # auto increment id
    task = {"id": new_id, "title": title_str, "done": False}

    TASKS.append(task)

    return task


@app.get("/tasks")
async def tasks():
    return TASKS


@app.get("/tasks/{id}")
async def tasks(id: int):
    task = next((t for t in TASKS if t["id"] == id), None)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
        )

    return task


@app.put("/tasks/{id}")
async def put_task(id: int, item: Item):
    task = next((t for t in TASKS if t["id"] == id), None)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
        )

    if item.title is None and item.done is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Empty/Invalid body"
        )

    task.update(item.model_dump(exclude_unset=True))

    return {"id": id, **task}

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    task = next((t for t in TASKS if t["id"] == id), None)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
        )

    TASKS.remove(task)
    
    return None 
