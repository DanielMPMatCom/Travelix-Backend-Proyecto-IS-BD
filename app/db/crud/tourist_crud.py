from fastapi import Depends, HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from models import TouristModel, UserModel
from schemas import TouristSchema, TouristCreateSchema
import db.crud.auth_crud as auth


def list_tourist(db: Session, skip: int, limit: int):
    return db.query(TouristModel).offset(skip).limit(limit).all()


def create_tourist(db: Session, tourist_create: TouristCreateSchema):
    user_exists = auth.get_user(db, tourist_create.username)
    if user_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # user = UserToModel(tourist_create)
    # db.add(user)
    # db.commit()
    # db.refresh(user)

    tourist = TouristToModel(tourist_create)
    db.add(tourist)
    db.commit()
    db.refresh(tourist)

    return "Success"


def get_tourist_me(db:Session, current_user = Depends(auth.get_current_active_user)) -> TouristSchema:  
    
    if current_user is  None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    tourist = db.query(TouristModel).filter(TouristModel.id == current_user.id).first()
    
    if tourist is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tourist data not found"
        )
    
    return ModelToSchema(current_user, tourist)


# def UserToModel(schema: TouristCreateSchema) -> UserModel:
#     return UserModel(
#         # id=schema.id,
#         username=schema.username,
#         name=schema.name,
#         phone=schema.phone,
#         email=schema.email,
#         role=schema.role,
#         password=auth.get_password_hash(schema.password)
#     )


def TouristToModel(schema: TouristCreateSchema) -> TouristModel:
    return TouristModel(
        # id=schema.id,
        username=schema.username,
        name=schema.name,
        phone=schema.phone,
        email=schema.email,
        role=schema.role,
        password=auth.get_password_hash(schema.password),
        nationality=schema.nationality,
        )

def ModelToSchema(user:UserModel, tourist:TouristModel) -> TouristSchema:
    return TouristSchema(
        id=user.id,
        username=user.username,
        name=user.name,
        phone=user.phone,
        email=user.email,
        role=user.role,
        nationality=tourist.nationality
    )
