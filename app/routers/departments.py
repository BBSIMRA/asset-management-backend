from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["Departments"])


@router.post("/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentBase, db: Session = Depends(get_db)):
    db_department = models.Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@router.get("/", response_model=List[schemas.Department])
def get_all_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()


@router.get("/{department_id}", response_model=schemas.Department)
def get_department_by_id(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(
        models.Department.department_id == department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return department


@router.put("/{department_id}", response_model=schemas.Department)
def update_department(
    department_id: int,
    updated_department: schemas.DepartmentBase,
    db: Session = Depends(get_db)
):
    department = db.query(models.Department).filter(
        models.Department.department_id == department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    for key, value in updated_department.model_dump().items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)
    return department


@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(
        models.Department.department_id == department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    db.delete(department)
    db.commit()

    return {"message": "Department deleted successfully"}