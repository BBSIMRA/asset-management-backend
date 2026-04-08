from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/api/assignments",
    tags=["Asset Assignments"]
)

@router.post("/", response_model=schemas.AssetAssignment)
def assign_asset(assignment: schemas.AssetAssignmentBase, db: Session = Depends(get_db)):
    """
    Assign an asset to an employee.
    """
    db_assignment = models.AssetAssignment(**assignment.model_dump())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.get("/", response_model=List[schemas.AssetAssignment])
def get_all_assignments(db: Session = Depends(get_db)):
    """
    Retrieve all asset assignments.
    """
    return db.query(models.AssetAssignment).all()


@router.get("/{assignment_id}", response_model=schemas.AssetAssignment)
def get_assignment_by_id(assignment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an assignment by ID.
    """
    assignment = db.query(models.AssetAssignment).filter(models.AssetAssignment.assignment_id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router.put("/{assignment_id}", response_model=schemas.AssetAssignment)
def update_assignment(assignment_id: int, updated_assignment: schemas.AssetAssignmentBase, db: Session = Depends(get_db)):
    """
    Update an existing assignment.
    """
    assignment = db.query(models.AssetAssignment).filter(models.AssetAssignment.assignment_id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    for key, value in updated_assignment.model_dump().items():
        setattr(assignment, key, value)

    db.commit()
    db.refresh(assignment)
    return assignment


@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """
    Delete an assignment by ID.
    """
    assignment = db.query(models.AssetAssignment).filter(models.AssetAssignment.assignment_id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}