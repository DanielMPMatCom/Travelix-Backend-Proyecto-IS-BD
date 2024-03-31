from fastapi import Depends, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from typing import List, Optional
from models import UserModel, AgentModel
from schemas import UserSchema, AgentSchema, AgentCreateSchema
import db.crud.auth_crud as auth

def list_agents(db:Session, skip:int=0, limit:int=1000):
    return db.query(AgentModel).filter(AgentModel.role == "agent").offset(skip).limit(limit).all()

def list_agents_by_agency(db:Session, agency_id:int, skip:int=0, limit:int=1000):
    return db.query(AgentModel).filter(AgentModel.agency_id == agency_id).\
        filter(AgentModel.role == "agent").offset(skip).limit(limit).all()

def list_marketing(db:Session, skip:int=0, limit:int=1000):
    return db.query(AgentModel).filter(AgentModel.role == "marketing").offset(skip).limit(limit).all()

def list_admins(db:Session, skip:int=0, limit:int=100):
    return db.query(UserModel).filter(UserModel.role == "admin").offset(skip).limit(limit).all()

def create_agent(db: Session, agent_create: AgentCreateSchema):
    user_exists = db.query(UserModel).filter(UserModel.username == agent_create.username).first()
    if user_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    agent = AgentToModel(agent_create, "agent")
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return "Success"

def create_marketing(db: Session, agent_create: AgentCreateSchema):
    user_exists = db.query(UserModel).filter(UserModel.username == agent_create.username).first()
    if user_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    agent = AgentToModel(agent_create, "marketing")
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return "Success"

def delete_agent(db: Session, agent_id: int):
    agent = get_agent(db, agent_id)
    
    if agent.role != "marketing" and agent.role != "agent":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"You are trying to delete {agent.role}")
    
    db.delete(agent)
    db.commit()
    
    return "Success"


def get_agent(db: Session, agent_id: int) -> AgentModel:
    agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    
    if agent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    
    return agent

def update_agent(db: Session, user_update: AgentSchema):
    user = db.query(UserModel).filter(UserModel.id == user_update.id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    UpdateAgent(user, user_update)
    
    db.commit()
    
    return "Success"

def get_agent_by_username(db: Session, username: str) -> AgentModel:
    agent = db.query(AgentModel).filter(AgentModel.username == username).first()
    
    if agent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    
    return agent

def AgentToModel(schema: AgentCreateSchema, role: str) -> AgentModel:
    return AgentModel(
        username=schema.username,
        name=schema.name,
        phone=schema.phone,
        email=schema.email,
        role=role,
        password=auth.get_password_hash(schema.password),
        agency_id=schema.agency_id
        )

def UpdateAgent(db: AgentModel, upd: AgentCreateSchema):
    if upd.username is not None:
        db.username = upd.username
    if upd.name is not None:
        db.name = upd.name
    if upd.phone is not None:
        db.phone = upd.phone
    if upd.email is not None:
        db.email = upd.email
    if upd.password is not None:
        db.password = auth.get_password_hash(upd.password)
    if upd.agency_id is not None:
        db.agency_id = upd.agency_id