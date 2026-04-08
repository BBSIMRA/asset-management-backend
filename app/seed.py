from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models
from datetime import date, datetime, timedelta

def seed_db():
    db = SessionLocal()
    try:
        # 1. Departments
        print("Seeding Departments...")
        departments = [
            models.Department(department_name="Engineering", department_code="ENG"),
            models.Department(department_name="Human Resources", department_code="HR"),
            models.Department(department_name="Finance", department_code="FIN"),
            models.Department(department_name="Marketing", department_code="MKT"),
            models.Department(department_name="Operations", department_code="OPS")
        ]
        db.add_all(departments)
        db.commit()

        # 2. HR Admins
        print("Seeding HR Admins...")
        hr_admins = [
            models.HRAdmin(admin_name="John Doe", email="john.doe@example.com", phone_number="1234567890", role="Senior HR"),
            models.HRAdmin(admin_name="Jane Smith", email="jane.smith@example.com", phone_number="0987654321", role="HR Manager"),
            models.HRAdmin(admin_name="Alice Johnson", email="alice.j@example.com", phone_number="1122334455", role="Admin"),
            models.HRAdmin(admin_name="Bob Brown", email="bob.b@example.com", phone_number="5544332211", role="Coordinator"),
            models.HRAdmin(admin_name="Charlie Davis", email="charlie.d@example.com", phone_number="6677889900", role="Lead HR")
        ]
        db.add_all(hr_admins)
        db.commit()

        # 3. Employees
        print("Seeding Employees...")
        employees = [
            models.Employee(employee_code="EMP001", first_name="Michael", last_name="Scott", email="michael.s@example.com", 
                            department_id=departments[0].department_id, designation="Lead Engineer", employment_status="Active", date_of_joining=date(2022, 1, 1)),
            models.Employee(employee_code="EMP002", first_name="Pam", last_name="Beesly", email="pam.b@example.com", 
                            department_id=departments[1].department_id, designation="HR Specialist", employment_status="Active", date_of_joining=date(2022, 2, 1)),
            models.Employee(employee_code="EMP003", first_name="Jim", last_name="Halpert", email="jim.h@example.com", 
                            department_id=departments[2].department_id, designation="Financial Analyst", employment_status="Active", date_of_joining=date(2022, 3, 1)),
            models.Employee(employee_code="EMP004", first_name="Dwight", last_name="Schrute", email="dwight.s@example.com", 
                            department_id=departments[3].department_id, designation="Marketing Lead", employment_status="Active", date_of_joining=date(2022, 4, 1)),
            models.Employee(employee_code="EMP005", first_name="Angela", last_name="Martin", email="angela.m@example.com", 
                            department_id=departments[4].department_id, designation="Ops Manager", employment_status="Active", date_of_joining=date(2022, 5, 1))
        ]
        db.add_all(employees)
        db.commit()

        # 4. Assets
        print("Seeding Assets...")
        assets = [
            models.Asset(asset_code="AST001", asset_name="MacBook Pro", asset_category="Laptop", purchase_date=date(2023, 1, 15), purchase_cost=2500.0, asset_status="Assigned", asset_condition="New"),
            models.Asset(asset_code="AST002", asset_name="Dell XPS 15", asset_category="Laptop", purchase_date=date(2023, 2, 10), purchase_cost=1800.0, asset_status="Assigned", asset_condition="Good"),
            models.Asset(asset_code="AST003", asset_name="iPhone 14", asset_category="Mobile", purchase_date=date(2023, 3, 5), purchase_cost=1000.0, asset_status="In Stock", asset_condition="New"),
            models.Asset(asset_code="AST004", asset_name="Herman Miller Chair", asset_category="Furniture", purchase_date=date(2023, 4, 20), purchase_cost=1200.0, asset_status="Assigned", asset_condition="New"),
            models.Asset(asset_code="AST005", asset_name="Monitor 27-inch", asset_category="Peripheral", purchase_date=date(2023, 5, 12), purchase_cost=400.0, asset_status="Retired", asset_condition="Damaged")
        ]
        db.add_all(assets)
        db.commit()

        # 5. Asset Assignments
        print("Seeding Asset Assignments...")
        assignments = [
            models.AssetAssignment(asset_id=assets[0].asset_id, employee_id=employees[0].employee_id, assigned_by_hr_id=hr_admins[0].hr_admin_id, assignment_date=date(2023, 6, 1), assignment_status="Active", remarks="Standard issue"),
            models.AssetAssignment(asset_id=assets[1].asset_id, employee_id=employees[1].employee_id, assigned_by_hr_id=hr_admins[1].hr_admin_id, assignment_date=date(2023, 6, 5), assignment_status="Active", remarks="Remote worker"),
            models.AssetAssignment(asset_id=assets[3].asset_id, employee_id=employees[2].employee_id, assigned_by_hr_id=hr_admins[2].hr_admin_id, assignment_date=date(2023, 6, 10), assignment_status="Returned", return_date=date(2023, 12, 1), remarks="Employee left"),
            models.AssetAssignment(asset_id=assets[0].asset_id, employee_id=employees[3].employee_id, assigned_by_hr_id=hr_admins[3].hr_admin_id, assignment_date=date(2023, 7, 1), assignment_status="Active", remarks="Project specific"),
            models.AssetAssignment(asset_id=assets[2].asset_id, employee_id=employees[4].employee_id, assigned_by_hr_id=hr_admins[4].hr_admin_id, assignment_date=date(2023, 7, 15), assignment_status="Active", remarks="Sales team")
        ]
        db.add_all(assignments)
        db.commit()

        # 6. Asset Maintenance Logs
        print("Seeding Asset Maintenance Logs...")
        logs = [
            models.AssetMaintenanceLog(asset_id=assets[0].asset_id, maintenance_type="Software update", maintenance_description="Updated OS and security patches", maintenance_cost=0.0, maintenance_date=date(2023, 8, 1), performed_by="IT Support"),
            models.AssetMaintenanceLog(asset_id=assets[1].asset_id, maintenance_type="Battery replacement", maintenance_description="Replaced faulty battery", maintenance_cost=150.0, maintenance_date=date(2023, 9, 10), performed_by="Dell Official"),
            models.AssetMaintenanceLog(asset_id=assets[4].asset_id, maintenance_type="Repair", maintenance_description="Fixed cracked screen", maintenance_cost=200.0, maintenance_date=date(2023, 10, 5), performed_by="Local Repair Shop"),
            models.AssetMaintenanceLog(asset_id=assets[0].asset_id, maintenance_type="Cleaning", maintenance_description="General internal cleaning", maintenance_cost=50.0, maintenance_date=date(2023, 11, 1), performed_by="IT Dept"),
            models.AssetMaintenanceLog(asset_id=assets[2].asset_id, maintenance_type="Checkup", maintenance_description="System diagnostics performed", maintenance_cost=25.0, maintenance_date=date(2023, 12, 10), performed_by="Internal Tech")
        ]
        db.add_all(logs)
        db.commit()

        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()