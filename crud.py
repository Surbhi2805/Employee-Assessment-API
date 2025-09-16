from bson import ObjectId
from datetime import datetime
from db import employees_collection

def emp_helper(doc):
    return {
        "id": str(doc["_id"]),
        "employee_id": doc["employee_id"],
        "name": doc["name"],
        "department": doc.get("department"),
        "salary": doc.get("salary"),
        "joining_date": doc.get("joining_date").date() if isinstance(doc.get("joining_date"), datetime) else doc.get("joining_date"),
        "skills": doc.get("skills", [])
    }
