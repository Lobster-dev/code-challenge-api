from fastapi import APIRouter, status, Depends
from src.api.auth import admin_required
from ..schemas import AgeGroupSchema
from typing import List
from src.services.age_groups import (
    create_age_group_service,
    delete_age_group_service,
    list_age_groups_service,
)

router = APIRouter(prefix="/age-groups", tags=["Age Groups"])

@router.post("/", response_model=AgeGroupSchema, status_code=status.HTTP_201_CREATED)
def create_age_group(age_group: AgeGroupSchema, user=Depends(admin_required)):
    return create_age_group_service(age_group)

@router.delete("/{age_group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_age_group(age_group_id: str, user=Depends(admin_required)):
    delete_age_group_service(age_group_id)
    return None

@router.get("/", response_model=List[AgeGroupSchema], status_code=status.HTTP_200_OK)
def list_age_groups(user=Depends(admin_required)):
    return list_age_groups_service()
