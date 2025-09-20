from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

security = HTTPBasic()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    users = {
        os.getenv("ADMIN_USERNAME"): {
            "password": os.getenv("ADMIN_PASSWORD"),
            "role": "admin"
        },
        os.getenv("USER_USERNAME"): {
            "password": os.getenv("USER_PASSWORD"),
            "role": "user"
        }
    }
    user_data = users.get(credentials.username)
    if not user_data or not user_data.get("password") or not secrets.compare_digest(credentials.password, user_data["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username, "role": user_data["role"]}

def admin_required(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required.")
    return current_user

def user_required(current_user=Depends(get_current_user)):
    if current_user["role"] != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User privileges required.")
    return current_user
