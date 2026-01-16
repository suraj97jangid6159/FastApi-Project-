from sqlalchemy.orm import Session
from .models import Employee

def create_employee(db: Session, emp):
    employee = Employee(**emp.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
