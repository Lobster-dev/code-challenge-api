from fastapi import APIRouter, status, Depends
from src.api.auth import user_required
from ..schemas import EnrollmentSchema
from typing import List
from src.services.enrollment import (
    request_enrollment_service,
    check_enrollment_status_service
)

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentSchema, status_code=status.HTTP_201_CREATED)
def request_enrollment(enrollment: EnrollmentSchema, user=Depends(user_required)):
    return request_enrollment_service(enrollment)


@router.get("/{cpf}", response_model=EnrollmentSchema, status_code=status.HTTP_200_OK)
def check_enrollment_status_by_cpf(cpf: str, user=Depends(user_required)):
    return check_enrollment_status_service(cpf)
