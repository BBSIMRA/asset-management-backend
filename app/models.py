from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String, nullable=False)
    department_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)  # Combined first_name and last_name
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    department_id = Column(Integer, ForeignKey("departments.department_id"))  # Keep department_id for relationships
    designation = Column(String)
    employment_status = Column(String)
    date_of_joining = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    department = relationship("Department", back_populates="employees")
    assignments = relationship("AssetAssignment", back_populates="employee")

class HRAdmin(Base):
    __tablename__ = "hr_admins"

    hr_admin_id = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    role = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    assignments = relationship("AssetAssignment", back_populates="assigned_by_hr")

class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)
    asset_code = Column(String, unique=True, index=True)
    asset_name = Column(String, nullable=False)
    asset_category = Column(String)
    purchase_date = Column(Date)
    purchase_cost = Column(Float)
    asset_status = Column(String)
    asset_condition = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    assignments = relationship("AssetAssignment", back_populates="asset")
    maintenance_logs = relationship("AssetMaintenanceLog", back_populates="asset")

class AssetAssignment(Base):
    __tablename__ = "asset_assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"))
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    assigned_by_hr_id = Column(Integer, ForeignKey("hr_admins.hr_admin_id"))
    assignment_date = Column(Date)
    return_date = Column(Date)
    assignment_status = Column(String)
    remarks = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    asset = relationship("Asset", back_populates="assignments")
    employee = relationship("Employee", back_populates="assignments")
    assigned_by_hr = relationship("HRAdmin", back_populates="assignments")

class AssetMaintenanceLog(Base):
    __tablename__ = "asset_maintenance_logs"

    maintenance_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"))
    maintenance_type = Column(String)
    maintenance_description = Column(Text)
    maintenance_cost = Column(Float)
    maintenance_date = Column(Date)
    performed_by = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    asset = relationship("Asset", back_populates="maintenance_logs")

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True)

    users = relationship("User", back_populates="role")


class Permission(Base):
    __tablename__ = "permissions"

    permission_id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String, unique=True)


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    permission_id = Column(Integer, ForeignKey("permissions.permission_id"))


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    role_id = Column(Integer, ForeignKey("roles.role_id"))

    role = relationship("Role", back_populates="users")