
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
USER_AUTH = ("user", "user")
ADMIN_AUTH = ("admin", "admin")

def test_create_enrollment():
    enrollment = {"name": "João Teste", "age": 18, "cpf": "123.456.789-99"}
    response = client.post("/api/v1/enrollments", json=enrollment, auth=USER_AUTH)
    assert response.status_code == 201

def test_enrollment_status():
    enrollment = {"name": "Maria Teste", "age": 20, "cpf": "987.654.321-00"}
    client.post("/api/v1/enrollments/", json=enrollment, auth=USER_AUTH)
    response = client.get(f"/api/v1/enrollments/{enrollment['cpf']}", auth=USER_AUTH)
    assert response.status_code in (200, 404)

def test_enrollment_auth():
    enrollment = {"name": "Ana Teste", "age": 22, "cpf": "111.222.333-44"}
    response = client.post("/api/v1/enrollments", json=enrollment, auth=ADMIN_AUTH)
    assert response.status_code == 403
