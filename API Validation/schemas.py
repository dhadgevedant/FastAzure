from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
import re


# BaseModel = Pydantic Model
# FastAPI will use this class to:
# 1. Check incoming data
# 2. Convert json into a py object
# 3. Return errors if any or save


class EmployeeCreate(BaseModel):
    # Required fields
    name: str
    email: EmailStr
    employee_id: str
    date_of_birth: date
    password: str

    # Optional field
    department: str | None = None

    # -----------------------------
    # id Checking
    # -----------------------------
    # EMO ID must be:
    # EMP-1234
    # EMP-5678
    # etc.
    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, value):

        pattern = r"^EMP-\d{4}$"

        if not re.match(pattern, value):
            raise ValueError(
                "Employee ID must be like EMP-1234"
            )

        return value

    # -----------------------------
    # Age Checking
    # -----------------------------
    @field_validator("date_of_birth")
    @classmethod
    def validate_age(cls, value):

        today = date.today()

        age = (
            today.year
            - value.year
            - (
                (today.month, today.day)
                < (value.month, value.day)
            )
        )

        if age < 18:
            raise ValueError(
                "Employee must be 18 or older"
            )

        return value