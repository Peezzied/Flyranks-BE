from fastapi import FastAPI, HTTPException, status

app = FastAPI()
TASKS = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Walk the dog", "done": True},
    {"id": 3, "title": "Read a book", "done": False},
]


@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/tasks")
async def tasks():
    return TASKS

@app.get("/tasks/{id}")
async def tasks(id: int):
    task = next((t for t in TASKS if t["id"] == id), None)
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {id} not found"
        )
    
    return task

