from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/api/maintenance",
    tags=["Asset Maintenance"]
)

@router.post("/", response_model=schemas.AssetMaintenanceLog)
def create_maintenance_log(log: schemas.AssetMaintenanceLogBase, db: Session = Depends(get_db)):
    """
    Create a maintenance log for an asset.
    """
    db_log = models.AssetMaintenanceLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get("/", response_model=List[schemas.AssetMaintenanceLog])
def get_all_maintenance_logs(db: Session = Depends(get_db)):
    """
    Retrieve all asset maintenance logs.
    """
    return db.query(models.AssetMaintenanceLog).all()


@router.get("/{maintenance_id}", response_model=schemas.AssetMaintenanceLog)
def get_maintenance_log_by_id(maintenance_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a maintenance log by ID.
    """
    log = db.query(models.AssetMaintenanceLog).filter(models.AssetMaintenanceLog.maintenance_id == maintenance_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    return log


@router.put("/{maintenance_id}", response_model=schemas.AssetMaintenanceLog)
def update_maintenance_log(maintenance_id: int, updated_log: schemas.AssetMaintenanceLogBase, db: Session = Depends(get_db)):
    """
    Update an existing maintenance log.
    """
    log = db.query(models.AssetMaintenanceLog).filter(models.AssetMaintenanceLog.maintenance_id == maintenance_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")

    for key, value in updated_log.model_dump().items():
        setattr(log, key, value)

    db.commit()
    db.refresh(log)
    return log


@router.delete("/{maintenance_id}")
def delete_maintenance_log(maintenance_id: int, db: Session = Depends(get_db)):
    """
    Delete a maintenance log by ID.
    """
    log = db.query(models.AssetMaintenanceLog).filter(models.AssetMaintenanceLog.maintenance_id == maintenance_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")

    db.delete(log)
    db.commit()
    return {"message": "Maintenance log deleted successfully"}