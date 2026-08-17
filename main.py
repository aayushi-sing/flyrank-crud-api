from fastapi import FastAPI, Response, HTTPException
import sqlite3
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
DB_NAME = "tasks.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)


    count = conn.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    if count == 0:
        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Connect SQLite database", 0),
                ("Test CRUD API", 0)
            ]
        )

    conn.commit()
    conn.close()

initialize_database()



class TaskCreate(BaseModel):
    title: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Test the API", "done": True}
]


@app.get("/", description="Get information about the Task API")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health", description="Check whether the API is running")
def health():
    return {"status": "ok"}

@app.get("/tasks", description="Get all tasks")
def get_tasks():
    conn = get_db_connection()

    rows = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.get("/tasks/{id}", description="Get a single task by ID")
def get_task(id: int):
    conn = get_db_connection()

    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return dict(row)

@app.post("/tasks", description="Create a new task")
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

@app.put("/tasks/{id}", description="Update an existing task")
def update_task(id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == id:
            if task_update.title is not None:
                if not task_update.title.strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )
                task["title"] = task_update.title.strip()

            if task_update.done is not None:
                task["done"] = task_update.done

            if task_update.title is None and task_update.done is None:
                return JSONResponse(
                    status_code=400,
                    content={"error": "At least one field is required"}
                )

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.delete(
    "/tasks/{id}",
    status_code=204,
    description="Delete a task by ID"
)
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )