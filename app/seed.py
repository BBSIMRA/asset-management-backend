from app import models
from datetime import date


def seed_data(db):

    # Departments
    if db.query(models.Department).count() == 0:
        db.add_all([
            models.Department(department_name="HR"),
            models.Department(department_name="IT"),
            models.Department(department_name="Finance")
        ])
        db.commit()

    # Employees
    if db.query(models.Employee).count() == 0:
        db.add(
            models.Employee(
                employee_code="EMP001",
                first_name="Rahul",
                last_name="Sharma",
                email="rahul@test.com",
                department_id=2,
                designation="Developer",
                employment_status="Active",
                date_of_joining=date.today()
            )
        )
        db.commit()

    # Assets
    if db.query(models.Asset).count() == 0:
        db.add_all([
            models.Asset(
                asset_tag="LAP001",
                asset_name="Dell Laptop",
                brand="Dell",
                model="Latitude",
                purchase_date=date.today(),
                asset_status="Available"
            ),
            models.Asset(
                asset_tag="MON001",
                asset_name="Monitor",
                brand="LG",
                model="24inch",
                purchase_date=date.today(),
                asset_status="Available"
            )
        ])
        db.commit()

    # Users
    if db.query(models.User).count() == 0:
        db.add_all([
            models.User(
                email="admin@test.com",
                password="admin123",
                role="HR"
            ),
            models.User(
                email="employee@test.com",
                password="emp123",
                role="EMPLOYEE"
            )
        ])
        db.commit()