from fastapi import APIRouter, HTTPException
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/register")
def register(request: RegisterRequest):
    try:
        return auth_service.register(
            request.username,
            request.email,
            request.password
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    try:
        return auth_service.login(
            request.email,
            request.password
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))