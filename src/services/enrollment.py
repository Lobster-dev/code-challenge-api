from src.api.schemas.enrollment import EnrollmentSchema
from fastapi import HTTPException
from typing import Optional
from src.db.mongo import enrollments_collection, age_groups_collection
from bson import ObjectId
from starlette import status



def request_enrollment_service(enrollment: EnrollmentSchema) -> EnrollmentSchema:
    # Verifica duplicidade de CPF
    if enrollments_collection.find_one({"cpf": enrollment.cpf}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já inscrito.")
    # Busca grupo etário compatível
    group = age_groups_collection.find_one({
        "min_age": {"$lte": enrollment.age},
        "max_age": {"$gte": enrollment.age}
    })
    if not group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não existe grupo etário para essa idade.")
    doc = enrollment.model_dump(exclude_unset=True)
    result = enrollments_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return EnrollmentSchema(**doc)

def check_enrollment_status_service(enrollment_id: str) -> Optional[EnrollmentSchema]:
    doc = enrollments_collection.find_one({"_id": ObjectId(enrollment_id)})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada.")
    doc["id"] = str(doc["_id"])
    return EnrollmentSchema(**doc)
