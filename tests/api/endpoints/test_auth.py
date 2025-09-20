
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

def test_admin_auth():
    response = client.get("/api/v1/age-groups", auth=ADMIN_AUTH)
    assert response.status_code == 200
    response = client.get("/api/v1/age-groups", auth=USER_AUTH)
    assert response.status_code == 403

def test_user_auth():
    enrollment = {"name": "Maria Teste", "age": 20, "cpf": "987.654.321-00"}
    response = client.post("/api/v1/enrollments", json=enrollment, auth=USER_AUTH)
    assert response.status_code == 201
    response = client.post("/api/v1/enrollments", json=enrollment, auth=ADMIN_AUTH)
    assert response.status_code == 403
