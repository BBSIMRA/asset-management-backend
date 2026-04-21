from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


# USERS
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

# DEPARTMENTS
class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String, unique=True)
    created_at = Column(DateTime, server_default=func.now())


# EMPLOYEES
class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    designation = Column(String)
    employment_status = Column(String)
    date_of_joining = Column(Date)
    created_at = Column(DateTime, server_default=func.now())


# ASSETS
class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String, unique=True)
    asset_name = Column(String)
    brand = Column(String)
    model = Column(String)
    purchase_date = Column(Date)
    asset_status = Column(String)
    created_at = Column(DateTime, server_default=func.now())


# ASSIGNMENTS
class AssetAssignment(Base):
    __tablename__ = "asset_assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"))
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    assigned_date = Column(Date)
    expected_return_date = Column(Date)
    actual_return_date = Column(Date)
    assignment_status = Column(String)
    created_at = Column(DateTime, server_default=func.now())


# MAINTENANCE
class AssetMaintenanceLog(Base):
    __tablename__ = "asset_maintenance_logs"

    maintenance_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"))
    maintenance_type = Column(String)
    maintenance_description = Column(Text)
    maintenance_cost = Column(Integer)
    maintenance_date = Column(Date)
    performed_by = Column(String)
    created_at = Column(DateTime, server_default=func.now())