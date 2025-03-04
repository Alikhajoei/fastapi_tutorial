from datetime import timedelta, datetime
from typing import Annotated
from fastapi import HTTPException,APIRouter,Path,Depends
from starlette import status
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt
router = APIRouter()


SECRET_KEY = "cf51f9b5a5d199540dcb6bbbf8f42d4dd999a22c892bd35a61535c56ad52153d"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency =  Annotated[Session,Depends(get_db)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRequest(BaseModel):
    username: str = Path(min_length=3, max_length=20)
    password: str = Path(min_length=8)



@router.post("/register/",status_code=status.HTTP_201_CREATED)
async def user_register(db: db_dependency,create_user_request: UserRequest):
    new_user,err = Users(username=create_user_request.username, hashed_password=pwd_context.hash(create_user_request.password),is_active=True)
    db.add(new_user)
    db.commit()
    return new_user,err if err else None

def create_access_token(username: str , user_id: int ,expires_delta: timedelta):
    to_encode = {"sub": username, "id": user_id}
    expire_at = datetime.now() + expires_delta
    to_encode.update({"exp": expire_at})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login/",status_code=status.HTTP_200_OK)
async def user_login(db: db_dependency,login_user_request: UserRequest):
    user = db.query(Users).filter(Users.username == login_user_request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not pwd_context.verify(login_user_request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return {"access_token": create_access_token(data={"sub": user.username})}