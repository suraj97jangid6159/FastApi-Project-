# fastapi-production-api


# Employee Management API

A simple **FastAPI** application to manage employees in a company, supporting **CRUD operations**, **JWT authentication**, **pagination**, **filtering**, and **error handling**.  

---

## Features

- **Create Employee**: Add new employee with unique email.
- **List Employees**: Paginated listing, with optional filtering by department and role.
- **Retrieve Employee**: Get employee by ID.
- **Update Employee**: Modify employee details.
- **Delete Employee**: Remove employee.
- **Authentication**: JWT token-based protection for all endpoints.
- **Validation**: Email uniqueness and required fields validated.
- **Error Handling**: Proper HTTP status codes (`201`, `204`, `400`, `401`, `404`).
- **Swagger Docs**: Interactive API documentation via `/docs`.

---

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite (default, can switch to PostgreSQL)
- JWT Authentication (python-jose)
- Pydantic for validation

---

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd employee_api
