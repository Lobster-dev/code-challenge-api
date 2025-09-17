from pydantic import BaseModel, Field
from typing import Optional

class EnrollmentSchema(BaseModel):
    id: Optional[str] = Field(None, example="507f1f77bcf86cd799439012")
    name: str = Field(..., example="João da Silva")
    age: int = Field(..., example=25)
    cpf: str = Field(..., example="123.456.789-00")
