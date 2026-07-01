from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Import our Pydantic model
from schemas import EmployeeCreate

app = FastAPI()

# Folder containing HTML files
templates = Jinja2Templates(directory="templates")

# Temporary storage
employees = []


# ----------------------------
# Home Page
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ----------------------------
# Create Employee
# ----------------------------
@app.post("/employees")
async def create_employee(
        employee: EmployeeCreate
):
    """
    employee: EmployeeCreate

    This is where Pydantic works.

    JSON received:

    {
        "name": "Vedant",
        "email": "abc@gmail.com",
        "employee_id": "EMP-1234",
        ...
    }

    becomes:

    employee.name
    employee.email
    employee.employee_id
    """

    # Convert Pydantic object to dictionary
    employee_dict = employee.model_dump()

    employees.append(employee_dict)

    return {
        "message": "Employee Added",
        "employee": employee_dict
    }


# ----------------------------
# Get All Employees
# ----------------------------
@app.get("/employees")
async def get_employees():
    return employees