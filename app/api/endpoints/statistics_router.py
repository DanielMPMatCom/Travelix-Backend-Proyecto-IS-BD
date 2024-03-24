from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from db.config import get_db

router = APIRouter(prefix="/statistics", tags=["statistics"])

