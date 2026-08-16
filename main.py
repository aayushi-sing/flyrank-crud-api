from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str | None = None

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Test the API", "done": True}
]


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.post("/tasks")
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )


    new_task = {
        "id": len(tasks) + 1,
        "title": task.title.strip(),
        "done": False
    }

    tasks.append(new_task)

    return JSONResponse(
        status_code=201,
        content=new_task
    )