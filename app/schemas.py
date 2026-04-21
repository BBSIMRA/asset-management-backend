from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, date
from typing import Optional


# =====================================================
# USERS / AUTH
# =====================================================

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str   # HR / EMPLOYEE


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# DEPARTMENTS
# =====================================================

class DepartmentBase(BaseModel):
    department_name: str


class Department(DepartmentBase):
    department_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# EMPLOYEES
# =====================================================

class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    department_id: int
    designation: Optional[str] = None
    employment_status: Optional[str] = "Active"
    date_of_joining: Optional[date] = None


class Employee(EmployeeBase):
    employee_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# ASSETS
# =====================================================

class AssetBase(BaseModel):
    asset_tag: str
    asset_name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    purchase_date: Optional[date] = None
    asset_status: Optional[str] = "Available"


class Asset(AssetBase):
    asset_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# ASSIGNMENTS
# =====================================================

class AssetAssignmentBase(BaseModel):
    asset_id: int
    employee_id: int
    assigned_date: Optional[date] = None
    expected_return_date: Optional[date] = None
    actual_return_date: Optional[date] = None
    assignment_status: Optional[str] = "Assigned"


class AssetAssignment(AssetAssignmentBase):
    assignment_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# MAINTENANCE
# =====================================================

class AssetMaintenanceLogBase(BaseModel):
    asset_id: int
    maintenance_type: str
    maintenance_description: Optional[str] = None
    maintenance_cost: Optional[int] = 0
    maintenance_date: Optional[date] = None
    performed_by: Optional[str] = None


class AssetMaintenanceLog(AssetMaintenanceLogBase):
    maintenance_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# DASHBOARD / STATS
# =====================================================

class DashboardStats(BaseModel):
    total_assets: int
    total_employees: int
    total_departments: int
    active_assignments: int
    total_maintenance: int


# =====================================================
# HEALTH
# =====================================================

class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: datetime


class UserLogin(BaseModel):
    email: str
    password: str
    role: str