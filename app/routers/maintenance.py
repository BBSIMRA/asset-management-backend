from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["Maintenance"])


# CREATE
@router.post("/", response_model=schemas.AssetMaintenanceLog)
def create_log(data: schemas.AssetMaintenanceLogBase, db: Session = Depends(get_db)):

    asset = db.query(models.Asset).filter(
        models.Asset.asset_id == data.asset_id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    log = models.AssetMaintenanceLog(**data.model_dump())

    db.add(log)

    asset.asset_status = "Under Maintenance"

    db.commit()
    db.refresh(log)

    return log


# GET ALL
@router.get("/", response_model=List[schemas.AssetMaintenanceLog])
def get_all_logs(db: Session = Depends(get_db)):
    return db.query(models.AssetMaintenanceLog).all()


# GET ONE
@router.get("/{maintenance_id}", response_model=schemas.AssetMaintenanceLog)
def get_log(maintenance_id: int, db: Session = Depends(get_db)):

    item = db.query(models.AssetMaintenanceLog).filter(
        models.AssetMaintenanceLog.maintenance_id == maintenance_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Log not found")

    return item


# UPDATE
@router.put("/{maintenance_id}", response_model=schemas.AssetMaintenanceLog)
def update_log(
    maintenance_id: int,
    data: schemas.AssetMaintenanceLogBase,
    db: Session = Depends(get_db)
):
    item = db.query(models.AssetMaintenanceLog).filter(
        models.AssetMaintenanceLog.maintenance_id == maintenance_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Log not found")

    for key, value in data.model_dump().items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


# DELETE
@router.delete("/{maintenance_id}")
def delete_log(maintenance_id: int, db: Session = Depends(get_db)):

    item = db.query(models.AssetMaintenanceLog).filter(
        models.AssetMaintenanceLog.maintenance_id == maintenance_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Log not found")

    asset = db.query(models.Asset).filter(
        models.Asset.asset_id == item.asset_id
    ).first()

    if asset:
        asset.asset_status = "Available"

    db.delete(item)
    db.commit()

    return {"message": "Deleted successfully"}