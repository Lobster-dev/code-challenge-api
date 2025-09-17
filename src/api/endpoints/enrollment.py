from fastapi import APIRouter, status
from ..schemas import EnrollmentSchema
from typing import List
from src.services.enrollment import (
    request_enrollment_service,
    check_enrollment_status_service,
)

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentSchema, status_code=status.HTTP_201_CREATED)
def request_enrollment(enrollment: EnrollmentSchema):
    return request_enrollment_service(enrollment)

@router.get("/{enrollment_id}", response_model=EnrollmentSchema, status_code=status.HTTP_200_OK)
def check_enrollment_status(enrollment_id: str):
    return check_enrollment_status_service(enrollment_id)
