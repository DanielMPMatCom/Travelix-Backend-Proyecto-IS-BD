from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.config import get_db

from schemas import TouristCreateSchema, TouristSchema, Token, TokenData, UserSchema
import db.crud.tourist_crud as crud
import db.crud.auth_crud as auth
from db.crud.auth_crud import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/role", response_model=str)
async def get_role(db: Session = Depends(get_db), current_user: UserSchema = Depends(auth.get_current_active_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return current_user.role