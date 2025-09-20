from fastapi import APIRouter, status, Depends
from src.api.auth import get_current_username
from ..schemas import EnrollmentSchema
from typing import List
from src.services.enrollment import (
    request_enrollment_service,
    check_enrollment_status_service
)

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentSchema, status_code=status.HTTP_201_CREATED)
def request_enrollment(enrollment: EnrollmentSchema, username: str = Depends(get_current_username)):
    return request_enrollment_service(enrollment)


@router.get("/{cpf}", response_model=EnrollmentSchema, status_code=status.HTTP_200_OK)
def check_enrollment_status_by_cpf(cpf: str, username: str = Depends(get_current_username)):
    return check_enrollment_status_service(cpf)
