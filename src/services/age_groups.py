from src.api.schemas.age_group import AgeGroupSchema
from fastapi import HTTPException
from typing import List
from src.db.mongo import age_groups_collection
from bson import ObjectId

def create_age_group_service(age_group: AgeGroupSchema) -> AgeGroupSchema:
    exists = age_groups_collection.find_one({
        "name": age_group.name,
        "min_age": age_group.min_age,
        "max_age": age_group.max_age
    })
    if exists:
        raise HTTPException(status_code=400, detail="Grupo já existe.")
    doc = age_group.model_dump(exclude_unset=True)
    result = age_groups_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return AgeGroupSchema(**doc)

def delete_age_group_service(age_group_id: str) -> None:
    result = age_groups_collection.delete_one({"_id": ObjectId(age_group_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")

def list_age_groups_service() -> List[AgeGroupSchema]:
    groups = []
    for doc in age_groups_collection.find():
        doc["id"] = str(doc["_id"])
        groups.append(AgeGroupSchema(**doc))
    return groups
