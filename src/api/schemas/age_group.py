from pydantic import BaseModel, Field
from typing import Optional

class AgeGroupSchema(BaseModel):
    id: Optional[str] = Field(None, example="507f1f77bcf86cd799439011")
    name: str = Field(..., example="Adulto")
    min_age: int = Field(..., example=18)
    max_age: int = Field(..., example=59)
