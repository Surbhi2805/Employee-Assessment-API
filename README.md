"Hello, this is my submission for the Employee Management API task.
I have built a REST API using FastAPI with MongoDB as the database."

🔹 Code Explanation

"In db.py, I have connected MongoDB using Motor, which is an async driver."

"In models.py, I used Pydantic schemas for request validation, such as EmployeeCreate and EmployeeUpdate."

"In main.py, I created different API routes for CRUD operations:

Create Employee

Get Employee by ID

Update Employee

Delete Employee

List employees by department

Calculate average salary by department

Search employees by skill"

🔹 Run & Demo

"Run the server using uvicorn main:app --reload."

(Show terminal → server running on http://127.0.0.1:8000)

"When I open Swagger UI at /docs, I can test all endpoints."

"For example, let’s create an employee." (Show POST /employees, send request → response JSON)

"Now I can fetch the employee by ID." (Show GET /employees/{employee_id})

"Finally, here is the average salary by department endpoint." (Show GET /employees/avg-salary result JSON)
