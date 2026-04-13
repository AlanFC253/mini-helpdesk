from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import Token
from app.core.security import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


FAKE_USER = {
    "username": "admin",
    "password": "123456",
}


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username != FAKE_USER["username"]
        or form_data.password != FAKE_USER["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(data={"sub": form_data.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }