from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)

@router.post("/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeBase, db: Session = Depends(get_db)):
    """
    Create a new employee.

    - Accepts department_name, converts it to department_id.
    - Returns the created employee record.
    """
    # Fetch department_id using department_name
    department = db.query(models.Department).filter(models.Department.department_name == employee.department_name).first()
    if not department:
        raise HTTPException(status_code=400, detail="Invalid department_name")

    # Create employee with department_id
    db_employee = models.Employee(
        **employee.model_dump(exclude={"department_name"}),
        department_id=department.department_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.get("/", response_model=List[schemas.Employee])
def get_all_employees(db: Session = Depends(get_db)):
    """
    Retrieve all employees.

    - Returns a list of all employees with department_name.
    """
    employees = db.query(
        models.Employee,
        models.Department.department_name
    ).join(models.Department, models.Employee.department_id == models.Department.department_id).all()

    # Map department_name into the response
    return [
        schemas.Employee(
            **employee.Employee.model_dump(),
            department_name=employee.department_name
        ) for employee in employees
    ]


@router.get("/{employee_id}", response_model=schemas.Employee)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single employee by ID.
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, updated_employee: schemas.EmployeeBase, db: Session = Depends(get_db)):
    """
    Update an existing employee's information.

    - Accepts department_name, converts it to department_id.
    - Updates the employee record.
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Fetch department_id using department_name
    if updated_employee.department_name:
        department = db.query(models.Department).filter(models.Department.department_name == updated_employee.department_name).first()
        if not department:
            raise HTTPException(status_code=400, detail="Invalid department_name")
        updated_employee_dict = updated_employee.model_dump(exclude={"department_name"})
        updated_employee_dict["department_id"] = department.department_id
    else:
        updated_employee_dict = updated_employee.model_dump()

    for key, value in updated_employee_dict.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee


@router.patch("/{employee_id}/status", response_model=schemas.Employee)
def deactivate_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Deactivate an employee by setting employment_status to 'Inactive'.
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.employment_status = "Inactive"
    db.commit()
    db.refresh(employee)
    return employee


@router.patch("/{employee_id}/status", response_model=schemas.Employee)
def deactivate_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Deactivate an employee by setting employment_status to 'Inactive'.
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.employment_status = "Inactive"
    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Delete an employee by ID.
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}