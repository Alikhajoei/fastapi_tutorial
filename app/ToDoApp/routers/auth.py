from fastapi import HTTPException,APIRouter,Path
from starlette import status


router = APIRouter()


@router.get("/register/",status_code=status.HTTP_201_CREATED)
async def register_user(username: str = Path( min_length=3, max_length=20), password: str = Path( min_length=8)):
    pass