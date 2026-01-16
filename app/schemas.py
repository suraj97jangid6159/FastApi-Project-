from pydantic import BaseModel, EmailStr
from datetime import date
from pydantic import EmailStr

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str | None = None
    role: str | None = None

class EmployeeResponse(EmployeeCreate):
    id: int
    date_joined: date

    class Config:
        orm_mode = True
