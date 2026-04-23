from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from fastapi.middleware.cors import CORSMiddleware

# ✅ IMPORT ROUTERS
from app.routers import assets, employees, departments, assignments, maintenance, users, auth

from app.seed import seed_data

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
allow_origins=["http://localhost:3000", "https://optiasset-frontend-roan.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Seed on startup
@app.on_event("startup")
def load_seed():
    db = SessionLocal()
    seed_data(db)
    db.close()


# ✅ INCLUDE ROUTERS (VERY IMPORTANT)
app.include_router(assets.router, prefix="/assets", tags=["Assets"])
app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(departments.router, prefix="/departments", tags=["Departments"])
app.include_router(assignments.router, prefix="/assignments", tags=["Assignments"])
app.include_router(maintenance.router, prefix="/maintenance", tags=["Maintenance"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Stats API
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "total_assets": db.query(models.Asset).count(),
        "total_employees": db.query(models.Employee).count(),
        "total_departments": db.query(models.Department).count(),
        "active_assignments": db.query(models.AssetAssignment).count(),
        "maintenance_logs": db.query(models.AssetMaintenanceLog).count()
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/logout/")
def logout():
    # Placeholder logic for logout
    return {"message": "User logged out successfully"}