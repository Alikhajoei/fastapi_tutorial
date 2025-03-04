from fastapi import HTTPException,APIRouter,Path
from starlette import status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRequest(BaseModel):
    username: str = Path(min_length=3, max_length=20)
    password: str = Path(min_length=8)



@router.post("/register/",status_code=status.HTTP_201_CREATED)
async def user_register(create_user_request: UserRequest):
    new_user = Users(username=create_user_request.username, hashed_password=pwd_context.hash(create_user_request.password),is_active=True)
    return new_user
