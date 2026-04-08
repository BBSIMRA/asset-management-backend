from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware  # ✅ ADDED

from app import models, database
from app.routers import employees, departments, assets, assignments, maintenance
from app.database import get_db

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="OptiAsset API",
    description="Asset Management System for Tessa Cloud Class",
    version="1.0.0"
)

# ✅ ADD THIS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- BASIC ENDPOINTS ----------------

@app.get("/")
def read_root():
    return {"message": "Tessa Cloud Class - OptiAsset API is running"}

@app.get("/about")
def read_about():
    return {"message": "OptiAsset - Asset Management System"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "departments": db.query(models.Department).count(),
        "employees": db.query(models.Employee).count(),
        "hr_admins": db.query(models.HRAdmin).count(),
        "assets": db.query(models.Asset).count(),
        "assignments": db.query(models.AssetAssignment).count(),
        "maintenance_logs": db.query(models.AssetMaintenanceLog).count(),
    }

# ---------------- ROUTER REGISTRATION ----------------

app.include_router(departments.router)
app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(maintenance.router)