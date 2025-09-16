from fastapi import FastAPI, HTTPException, status, Query
from models import EmployeeCreate, EmployeeUpdate
from db import employees_collection
from crud import emp_helper
from datetime import datetime, time

app = FastAPI(title="Employee Assessment API")

@app.post("/employees", status_code=201)
async def create_employee(emp: EmployeeCreate):
    exists = await employees_collection.find_one({"employee_id": emp.employee_id})
    if exists:
        raise HTTPException(status_code=400, detail="employee_id already exists")
    jd = datetime.combine(emp.joining_date, time.min)
    doc = emp.dict()
    doc["joining_date"] = jd
    res = await employees_collection.insert_one(doc)
    created = await employees_collection.find_one({"_id": res.inserted_id})
    return emp_helper(created)

@app.get("/employees/avg-salary")
async def avg_salary_by_dept():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"department": "$_id", "avg_salary": {"$round": ["$avg_salary", 0]}, "_id": 0}}
    ]
    cursor = employees_collection.aggregate(pipeline)
    out = []
    async for doc in cursor:
        out.append(doc)
    return out


@app.get("/employees/search")
async def search_by_skill(skill: str = Query(...)):
    # Case-insensitive exact match in array
    cursor = employees_collection.find({
        "skills": {"$elemMatch": {"$regex": f"^{skill}$", "$options": "i"}}
    })

    out = []
    async for doc in cursor:
        out.append(emp_helper(doc))

    if not out:
        raise HTTPException(status_code=404, detail="Employee not found")

    return out


@app.get("/employees/{employee_id}")
async def get_employee(employee_id: str):
    doc = await employees_collection.find_one({"employee_id": employee_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp_helper(doc)

@app.put("/employees/{employee_id}")
async def update_employee(employee_id: str, emp: EmployeeUpdate):
    update_data = emp.dict(exclude_unset=True)
    if "joining_date" in update_data:
        update_data["joining_date"] = datetime.combine(update_data["joining_date"], time.min)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    result = await employees_collection.update_one({"employee_id": employee_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    updated = await employees_collection.find_one({"employee_id": employee_id})
    return emp_helper(updated)

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    res = await employees_collection.delete_one({"employee_id": employee_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Employee deleted successfully"}

@app.get("/employees")
async def list_employees(department: str = Query(None, description="Department name to filter")):
    query = {}
    if department:
        query["department"] = department
    cursor = employees_collection.find(query).sort("joining_date", -1)
    results = []
    async for doc in cursor:
        results.append(emp_helper(doc))
    return results

