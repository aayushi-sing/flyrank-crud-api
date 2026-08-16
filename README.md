# FlyRank CRUD Task API

A small REST API built with Python and FastAPI for managing a to-do task list.  
This project was built as part of the FlyRank Backend Track Week 2 Assignment 1.

The API implements the four CRUD operations:
- Create tasks
- Read tasks
- Update tasks
- Delete tasks

Data is stored in memory, so it resets when the server restarts. No database is used.

## Tech Stack
- Python
- FastAPI
- Uvicorn
- Pydantic
- Swagger UI / OpenAPI

## Installation

Clone the repository and enter the project directory:

```bash
cd flyrank-crud-api
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

Start the server with:

```bash
uvicorn main:app --reload
```

The API will be available at:

http://localhost:8000

Swagger UI is available at:

http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description | Success |
|--------|----------|--------------|---------|
| GET | / | Get API information | 200 |
| GET | /health | Check API health | 200 |
| GET | /tasks | Get all tasks | 200 |
| GET | /tasks/{id} | Get a task by ID | 200 |
| POST | /tasks | Create a new task | 201 |
| PUT | /tasks/{id} | Update an existing task | 200 |
| DELETE | /tasks/{id} | Delete a task | 204 |

## Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Invalid or empty request body |
| 404 | Task ID does not exist |

## Example API Request

Get all tasks:

```bash
curl.exe -i http://localhost:8000/tasks
```

Example response:

```text
HTTP/1.1 200 OK
content-type: application/json

[{"id":1,"title":"Learn FastAPI","done":false},{"id":2,"title":"Build CRUD API","done":false},{"id":3,"title":"Test the API","done":true}]
```

## Swagger UI

The API includes automatically generated Swagger documentation using FastAPI.

Open Swagger UI at:

http://localhost:8000/docs

![Swagger UI](screenshots/swagger-ui.png)

## Project Structure
flyrank-crud-api/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
    └── swagger-ui.png

## Notes

This project intentionally uses an in-memory list instead of a database, as required for this assignment. Therefore, tasks created during a server session are lost when the server restarts.