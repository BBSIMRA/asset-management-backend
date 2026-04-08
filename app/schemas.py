from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional

# =========================
# Base Schemas (Shared)
# =========================

class DepartmentBase(BaseModel):
    department_name: str
    department_code: str


class EmployeeBase(BaseModel):
    employee_code: str
    name: str  # Combined first_name and last_name
    email: str
    phone_number: Optional[str] = None
    department_name: str  # Replace department_id with department_name
    designation: Optional[str] = None
    employment_status: Optional[str] = None
    date_of_joining: Optional[date] = None


class HRAdminBase(BaseModel):
    admin_name: str
    email: str
    phone_number: Optional[str] = None
    role: Optional[str] = None


class AssetBase(BaseModel):
    asset_code: str
    asset_name: str
    asset_category: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_cost: Optional[float] = None
    asset_status: Optional[str] = None
    asset_condition: Optional[str] = None


class AssetAssignmentBase(BaseModel):
    asset_id: int
    employee_id: int
    assigned_by_hr_id: int
    assignment_date: Optional[date] = None
    return_date: Optional[date] = None
    assignment_status: Optional[str] = None
    remarks: Optional[str] = None


class AssetMaintenanceLogBase(BaseModel):
    asset_id: int
    maintenance_type: Optional[str] = None
    maintenance_description: Optional[str] = None
    maintenance_cost: Optional[float] = None
    maintenance_date: Optional[date] = None
    performed_by: Optional[str] = None


# =========================
# Response Schemas
# =========================

class Department(DepartmentBase):
    department_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Employee(EmployeeBase):
    employee_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HRAdmin(HRAdminBase):
    hr_admin_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Asset(AssetBase):
    asset_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssetAssignment(AssetAssignmentBase):
    assignment_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssetMaintenanceLog(AssetMaintenanceLogBase):
    maintenance_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)