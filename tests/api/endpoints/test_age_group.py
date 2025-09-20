
import pytest
import os
# Garante que as variáveis de ambiente estejam corretas para os testes
os.environ.setdefault("ADMIN_USERNAME", "admin")
os.environ.setdefault("ADMIN_PASSWORD", "admin")
os.environ.setdefault("USER_USERNAME", "user")
os.environ.setdefault("USER_PASSWORD", "user")
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)
ADMIN_AUTH = ("admin", "admin")
USER_AUTH = ("user", "user")

def test_create_age_group():
    data = {"name": "Jovem", "min_age": 12, "max_age": 17}
    response = client.post("/api/v1/age-groups", json=data, auth=ADMIN_AUTH)
    assert response.status_code == 201
    assert response.json()["name"] == "Jovem"

def test_list_age_groups():
    response = client.get("/api/v1/age-groups", auth=ADMIN_AUTH)
    assert response.status_code == 200

def test_delete_age_group():
    data = {"name": "Temp", "min_age": 1, "max_age": 10}
    resp = client.post("/api/v1/age-groups", json=data, auth=ADMIN_AUTH)
    group_id = resp.json()["id"]
    response = client.delete(f"/api/v1/age-groups/{group_id}", auth=ADMIN_AUTH)
    assert response.status_code == 204

def test_age_group_auth():
    response = client.get("/api/v1/age-groups", auth=USER_AUTH)
    assert response.status_code == 403
