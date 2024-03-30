from fastapi import Depends, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from typing import List, Optional
from models import UserModel
from schemas import UserSchema, UserCreateSchema
import db.crud.auth_crud as auth

def list_agents(db:Session, skip:int=0, limit:int=100):
    return db.query(UserModel).filter(UserModel.role == "agent").offset(skip).limit(limit).all()

def list_marketing(db:Session, skip:int=0, limit:int=100):
    return db.query(UserModel).filter(UserModel.role == "marketing").offset(skip).limit(limit).all()

def list_admins(db:Session, skip:int=0, limit:int=100):
    return db.query(UserModel).filter(UserModel.role == "admin").offset(skip).limit(limit).all()

def create_agent(db: Session, user_create: UserCreateSchema):
    user_exists = db.query(UserModel).filter(UserModel.username == user_create.username).first()
    if user_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user = UserModel(username=user_create.username, password=auth.get_password_hash(user_create.password), role="agent")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return "Success"

def create_marketing(db: Session, user_create: UserCreateSchema):
    user_exists = db.query(UserModel).filter(UserModel.username == user_create.username).first()
    if user_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user = UserModel(username=user_create.username, password=auth.get_password_hash(user_create.password), role="marketing")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return "Success"

def delete_agent(db: Session, agent_id: int):
    agent = db.query(UserModel).filter(UserModel.id == agent_id).first()
    if agent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    if agent.role != "agent":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not an agent")
    
    db.delete(agent)
    db.commit()
    
    return "Success"

def delete_marketing(db: Session, marketing_id: int):
    marketing = db.query(UserModel).filter(UserModel.id == marketing_id).first()
    if marketing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marketing not found")
    if marketing.role != "marketing":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a marketing dude")

    db.delete(marketing)
    db.commit()
    
    return "Success"

def update_user(db: Session, user_update: UserSchema):
    user = db.query(UserModel).filter(UserModel.id == user_update.id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.username = user_update.username
    user.password = auth.get_password_hash(user_update.password)
    
    db.commit()
    
    return "Success"