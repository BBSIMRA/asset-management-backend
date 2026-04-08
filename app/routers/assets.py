from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.dependencies import RequirePrivilege

router = APIRouter(
    prefix="/api/assets",
    tags=["Assets"]
)

@router.post("/", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetBase, db: Session = Depends(get_db)):
    """
    Create a new asset.
    """
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.get("/", response_model=List[schemas.Asset])
def get_all_assets(db: Session = Depends(get_db)):
    """
    Retrieve all assets.
    """
    return db.query(models.Asset).all()


@router.get("/{asset_id}", response_model=schemas.Asset)
def get_asset_by_id(asset_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an asset by ID.
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.put("/{asset_id}", response_model=schemas.Asset)
def update_asset(asset_id: int, updated_asset: schemas.AssetBase, db: Session = Depends(get_db)):
    """
    Update an existing asset.
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    for key, value in updated_asset.model_dump().items():
        setattr(asset, key, value)

    db.commit()
    db.refresh(asset)
    return asset


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    allowed: bool = Depends(RequirePrivilege("delete:asset")),
    db: Session = Depends(get_db)
):
    asset = db.query(models.Asset).filter(models.Asset.asset_id == asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    db.delete(asset)
    db.commit()

    return {"message": f"Asset {asset_id} deleted"}