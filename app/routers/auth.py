from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email")

    if existing_user.password != user.password:
        raise HTTPException(status_code=401, detail="Wrong password")

    if existing_user.role != user.role:
        raise HTTPException(status_code=401, detail="Wrong role selected")

    return {
        "message": "Login successful",
        "role": existing_user.role,
        "name": existing_user.name,
        "user_id": existing_user.user_id
    }