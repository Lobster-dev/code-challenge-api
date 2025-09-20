from pydantic import BaseModel, Field
from typing import Optional

class EnrollmentSchema(BaseModel):
    id: Optional[str] = Field(None, json_schema_extra={"example": "507f1f77bcf86cd799439012"})
    name: str = Field(..., json_schema_extra={"example": "João da Silva"})
    age: int = Field(..., json_schema_extra={"example": 25})
    cpf: str = Field(..., json_schema_extra={"example": "123.456.789-00"})
