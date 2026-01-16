from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app import models, schemas, crud, auth
from app.auth import create_access_token, fake_user

# -------------------------------
# App initialization
# -------------------------------
app = FastAPI(title="Employee Management API")

Base.metadata.create_all(bind=engine)

# -------------------------------
# Database dependency
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# Auth / Token endpoint
# -------------------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username != fake_user["username"]
        or form_data.password != fake_user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        data={"sub": form_data.username}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

# -------------------------------
# Employee APIs (Protected)
# -------------------------------
@app.post(
    "/api/employees/",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    user: str = Depends(auth.get_current_user),
):
    if db.query(models.Employee).filter(
        models.Employee.email == employee.email
    ).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    return crud.create_employee(db, employee)


@app.get("/api/employees/", response_model=list[schemas.EmployeeResponse])
def list_employees(
    page: int = 1,
    department: str | None = None,
    role: str | None = None,
    db: Session = Depends(get_db),
    user: str = Depends(auth.get_current_user),
):
    query = db.query(models.Employee)

    if department:
        query = query.filter(models.Employee.department == department)
    if role:
        query = query.filter(models.Employee.role == role)

    return query.offset((page - 1) * 10).limit(10).all()


@app.get("/api/employees/{id}/", response_model=schemas.EmployeeResponse)
def get_employee(
    id: int,
    db: Session = Depends(get_db),
    user: str = Depends(auth.get_current_user),
):
    emp = db.get(models.Employee, id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@app.put("/api/employees/{id}/", response_model=schemas.EmployeeResponse)
def update_employee(
    id: int,
    emp: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    user: str = Depends(auth.get_current_user),
):
    employee = db.get(models.Employee, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in emp.dict().items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee


@app.delete("/api/employees/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    id: int,
    db: Session = Depends(get_db),
    user: str = Depends(auth.get_current_user),
):
    emp = db.get(models.Employee, id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()
