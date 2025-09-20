from pydantic import BaseModel, Field
from typing import Optional

class AgeGroupSchema(BaseModel):
    id: Optional[str] = Field(None, json_schema_extra={"example": "507f1f77bcf86cd799439011"})
    name: str = Field(..., json_schema_extra={"example": "Adulto"})
    min_age: int = Field(..., json_schema_extra={"example": 18})
    max_age: int = Field(..., json_schema_extra={"example": 59})
