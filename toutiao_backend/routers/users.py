from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from crud import users
from models.users import User
from config.db_conf import get_db
from schemas.users import UserRequest
from starlette import status
router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
  # 注册逻辑:验证用户是否存在 ->创建用户 -> 生成Token -> 响应结果
  existing_user =  await users.get_user_by_username(db, user_data.username)
  if existing_user:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已经存在")
  user = await users.create_user(db, user_data)
  return {
      "code": 200,
      "message": "注册成功",
      "data": {
        "token": "用户访问令牌",
        "userInfo": {
          "id": user.id,
          "username": user.username,
          "bio": user.bio,
          "avatar": user.avatar
        }
      }
    }
