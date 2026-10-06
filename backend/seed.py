"""
SmartERP - HR Seed Script
Creates sample departments and employees for development.
Run: python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database.database import SessionLocal, engine, Base
from app.models.department import Department
from app.models.employee import Employee, EmployeeStatus, Gender
from app.models.attendance import Attendance, AttendanceStatus
from app.models.leave import Leave, LeaveType, LeaveStatus
from datetime import date, timedelta, time

Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed():
    print("🌱 Seeding HR data...")

    # ── Departments ────────────────────────────────────────────────────────
    dept_data = [
        {"name": "Human Resources",    "code": "HR",      "description": "HR & People Operations"},
        {"name": "Engineering",         "code": "ENG",     "description": "Software Development"},
        {"name": "Finance",             "code": "FIN",     "description": "Finance & Accounting"},
        {"name": "Marketing",           "code": "MKT",     "description": "Marketing & Growth"},
        {"name": "Sales",               "code": "SLS",     "description": "Sales & Revenue"},
        {"name": "Operations",          "code": "OPS",     "description": "Business Operations"},
    ]

    depts = {}
    for d in dept_data:
        existing = db.query(Department).filter(Department.name == d["name"]).first()
        if not existing:
            dept = Department(**d)
            db.add(dept)
            db.flush()
            depts[d["code"]] = dept
            print(f"  ✅ Department: {d['name']}")
        else:
            depts[d["code"]] = existing
    db.commit()

    # ── Employees ──────────────────────────────────────────────────────────
    employees_data = [
        {
            "employee_id": "EMP0001", "first_name": "Alice",  "last_name": "Johnson",
            "email": "alice.johnson@smarterp.com", "phone": "+1-555-0101",
            "job_title": "HR Manager", "department_id": depts["HR"].id,
            "hire_date": date(2022, 1, 15), "salary": 75000, "status": EmployeeStatus.ACTIVE,
            "gender": Gender.FEMALE,
        },
        {
            "employee_id": "EMP0002", "first_name": "Bob",    "last_name": "Smith",
            "email": "bob.smith@smarterp.com", "phone": "+1-555-0102",
            "job_title": "Senior Software Engineer", "department_id": depts["ENG"].id,
            "hire_date": date(2021, 6, 1), "salary": 95000, "status": EmployeeStatus.ACTIVE,
            "gender": Gender.MALE,
        },
        {
            "employee_id": "EMP0003", "first_name": "Carol",  "last_name": "Williams",
            "email": "carol.williams@smarterp.com", "phone": "+1-555-0103",
            "job_title": "Finance Analyst", "department_id": depts["FIN"].id,
            "hire_date": date(2023, 3, 20), "salary": 68000, "status": EmployeeStatus.ACTIVE,
            "gender": Gender.FEMALE,
        },
        {
            "employee_id": "EMP0004", "first_name": "David",  "last_name": "Brown",
            "email": "david.brown@smarterp.com", "phone": "+1-555-0104",
            "job_title": "Marketing Specialist", "department_id": depts["MKT"].id,
            "hire_date": date(2022, 9, 10), "salary": 60000, "status": EmployeeStatus.ACTIVE,
            "gender": Gender.MALE,
        },
        {
            "employee_id": "EMP0005", "first_name": "Eva",    "last_name": "Martinez",
            "email": "eva.martinez@smarterp.com", "phone": "+1-555-0105",
            "job_title": "Sales Representative", "department_id": depts["SLS"].id,
            "hire_date": date(2023, 7, 5), "salary": 55000, "status": EmployeeStatus.ACTIVE,
            "gender": Gender.FEMALE,
        },
    ]

    employees = {}
    for e in employees_data:
        existing = db.query(Employee).filter(Employee.employee_id == e["employee_id"]).first()
        if not existing:
            emp = Employee(**e)
            db.add(emp)
            db.flush()
            employees[e["employee_id"]] = emp
            print(f"  ✅ Employee: {e['first_name']} {e['last_name']}")
        else:
            employees[e["employee_id"]] = existing
    db.commit()

    # ── Attendance (last 7 days) ───────────────────────────────────────────
    today = date.today()
    statuses = [AttendanceStatus.PRESENT, AttendanceStatus.PRESENT, AttendanceStatus.LATE,
                AttendanceStatus.PRESENT, AttendanceStatus.HALF_DAY]
    for i, (key, emp) in enumerate(employees.items()):
        for day_offset in range(7):
            att_date = today - timedelta(days=day_offset)
            existing = db.query(Attendance).filter(
                Attendance.employee_id == emp.id,
                Attendance.date == att_date
            ).first()
            if not existing:
                db.add(Attendance(
                    employee_id=emp.id,
                    date=att_date,
                    check_in=time(9, 0),
                    check_out=time(18, 0),
                    status=statuses[i % len(statuses)],
                ))
    db.commit()
    print("  ✅ Attendance records added")

    # ── Leave requests ─────────────────────────────────────────────────────
    emp1 = list(employees.values())[0]
    emp2 = list(employees.values())[1]
    if not db.query(Leave).filter(Leave.employee_id == emp1.id).first():
        db.add(Leave(
            employee_id=emp1.id,
            leave_type=LeaveType.ANNUAL,
            start_date=today + timedelta(days=5),
            end_date=today + timedelta(days=7),
            total_days=3,
            reason="Family vacation",
            status=LeaveStatus.PENDING,
        ))
    if not db.query(Leave).filter(Leave.employee_id == emp2.id).first():
        db.add(Leave(
            employee_id=emp2.id,
            leave_type=LeaveType.SICK,
            start_date=today - timedelta(days=3),
            end_date=today - timedelta(days=2),
            total_days=2,
            reason="Flu",
            status=LeaveStatus.APPROVED,
            reviewed_by=1,
        ))
    db.commit()
    print("  ✅ Leave requests added")

    print("\n✨ HR seed complete!")
    print("   Departments:", db.query(Department).count())
    print("   Employees:  ", db.query(Employee).count())
    print("   Attendance: ", db.query(Attendance).count())
    print("   Leaves:     ", db.query(Leave).count())

if __name__ == "__main__":
    seed()
    db.close()
