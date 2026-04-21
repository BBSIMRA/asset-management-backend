from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["Employees"])


# CREATE
@router.post("/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeBase, db: Session = Depends(get_db)):
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


# GET ALL
@router.get("/", response_model=List[schemas.Employee])
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()


# GET ONE
@router.get("/{employee_id}", response_model=schemas.Employee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


# UPDATE
@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    employee_id: int,
    data: schemas.EmployeeBase,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in data.model_dump().items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


# PATCH STATUS
@router.patch("/{employee_id}/status", response_model=schemas.Employee)
def patch_employee_status(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.employment_status = "Inactive"

    db.commit()
    db.refresh(employee)

    return employee


# DELETE
@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}