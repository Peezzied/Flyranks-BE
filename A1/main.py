from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import storage

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
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "title is required and cannot be empty"},
        )
    return storage.create_task(title.strip())


@app.get("/tasks")
async def tasks(search: str | None = None, done: bool | None = None):
    filtered_tasks = storage.get_tasks()
    
    if search is not None:
        filtered_tasks = [i for i in filtered_tasks if search.lower() in i.title.lower() ]
        
    if done is not None:
        filtered_tasks = [i for i in filtered_tasks if i.done == done ]
    
    return filtered_tasks


@app.get("/tasks/{id}")
async def tasks(id: int):
    task = storage.get_task(id)

    if not task:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {id} not found"},
        )

    return task


@app.put("/tasks/{id}")
async def put_task(id: int, item: Item):
    task = storage.get_task(id)

    if not task:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=f"Task {id} not found"
        )

    if not item.title and not item.done:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="request body must include title and/or done",
        )

    task.update(item.model_dump(exclude_unset=True))

    return {"id": id, **task}


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    task = next((t for t in TASKS if t["id"] == id), None)

    if task is None:
        raise JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=f"Task {id} not found"
        )

    TASKS.remove(task)

    return None

if __name__ == "__main__":
    storage.create_db_and_tables()
    storage.populate_db()