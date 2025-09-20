from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

security = HTTPBasic()


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
USER_USERNAME = os.getenv("USER_USERNAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")

USERS = {
    ADMIN_USERNAME: {
        "password": ADMIN_PASSWORD,
        "role": "admin"
    },
    USER_USERNAME: {
        "password": USER_PASSWORD,
        "role": "user"
    }
}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = USERS.get(credentials.username)
    if not user or not secrets.compare_digest(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username, "role": user["role"]}

def admin_required(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required.")
    return current_user

def user_required(current_user=Depends(get_current_user)):
    if current_user["role"] != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User privileges required.")
    return current_user
