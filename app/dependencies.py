from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RequirePrivilege:
    def __init__(self, permission: str):
        self.permission = permission

    def __call__(self):
        # TEMP user simulation
        current_user_role = "Admin"

        role_permissions = {
            "Admin": [
                "delete:asset",
                "view:inventory",
                "create:asset",
                "assign:asset"
            ],
            "Employee": [
                "view:my_gear"
            ]
        }

        if self.permission not in role_permissions.get(current_user_role, []):
            raise HTTPException(status_code=403, detail="Permission denied")

        return True