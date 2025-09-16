from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class EmployeeCreate(BaseModel):
    employee_id: str = Field(..., min_length=1)
    name: str
    department: str
    salary: int
    joining_date: date
    skills: List[str]

class EmployeeUpdate(BaseModel):
    name: Optional[str]
    department: Optional[str]
    salary: Optional[int]
    joining_date: Optional[date]
    skills: Optional[List[str]]

class EmployeeOut(BaseModel):
    id: str
    employee_id: str
    name: str
    department: str
    salary: int
    joining_date: date
    skills: List[str]
