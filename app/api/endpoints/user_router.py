from fastapi import APIRouter, HTTPException, Path, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.config import get_db

from schemas import AgentSchema, AgentCreateSchema, Token, TokenData, UserSchema, UserCreateSchema
from models import UserModel
import db.crud.user_crud as crud
import db.crud.auth_crud as auth
from db.crud.auth_crud import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/role", response_model=str)
async def get_role(current_user: UserSchema = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return current_user.role

@router.post("/create/agent/{marketing_id}", response_model=str)
async def create_agent_by_id(agent: AgentCreateSchema, marketing_id: int, db: Session = Depends(get_db)):
    # if current_user.role != "marketing":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The current user has no permisson to perform this action")
    
    agent.role = "agent"
    agent.agency_id = crud.get_agent(db, marketing_id).agency_id    

    return crud.create_agent(db, agent)

@router.post("/create/agent", response_model=str)
async def create_agent(agent: AgentCreateSchema, db: Session = Depends(get_db)):

    if agent.role != "agent" and agent.role != "marketing":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{agent.role} is not a valid role")

    return crud.create_agent(db, agent) if agent.role == "agent" else crud.create_marketing(db, agent)


@router.get("/list")
async def list_users(db: Session = Depends(get_db)):
    return crud.list_agents(db) + crud.list_marketing(db)

@router.get("/list/{agency_id}")
async def list_agents_by_agency(agency_id:int, db: Session = Depends(get_db)):
    return crud.list_agents_by_agency(db, agency_id)

@router.get("/delete/{agent_id}")
async def delete_user(agent_id:int, db: Session = Depends(get_db)):
    return crud.delete_agent(db, agent_id)