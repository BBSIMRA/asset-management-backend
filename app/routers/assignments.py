from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["Assignments"])


# CREATE
@router.post("/", response_model=schemas.AssetAssignment)
def create_assignment(data: schemas.AssetAssignmentBase, db: Session = Depends(get_db)):

    asset = db.query(models.Asset).filter(
        models.Asset.asset_id == data.asset_id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == data.employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    assignment = models.AssetAssignment(**data.model_dump())

    db.add(assignment)

    asset.asset_status = "Assigned"

    db.commit()
    db.refresh(assignment)

    return assignment


# GET ALL
@router.get("/", response_model=List[schemas.AssetAssignment])
def get_all_assignments(db: Session = Depends(get_db)):
    return db.query(models.AssetAssignment).all()


# GET ONE
@router.get("/{assignment_id}", response_model=schemas.AssetAssignment)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):

    item = db.query(models.AssetAssignment).filter(
        models.AssetAssignment.assignment_id == assignment_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return item


# UPDATE
@router.put("/{assignment_id}", response_model=schemas.AssetAssignment)
def update_assignment(
    assignment_id: int,
    data: schemas.AssetAssignmentBase,
    db: Session = Depends(get_db)
):

    item = db.query(models.AssetAssignment).filter(
        models.AssetAssignment.assignment_id == assignment_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Assignment not found")

    for key, value in data.model_dump().items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


# DELETE
@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):

    item = db.query(models.AssetAssignment).filter(
        models.AssetAssignment.assignment_id == assignment_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Assignment not found")

    asset = db.query(models.Asset).filter(
        models.Asset.asset_id == item.asset_id
    ).first()

    if asset:
        asset.asset_status = "Available"

    db.delete(item)
    db.commit()

    return {"message": "Deleted successfully"}