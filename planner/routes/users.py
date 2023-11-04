# 사용자 등록 및 로그인 처리를 위한 라우팅
from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_router = APIRouter(
    tags=["User"],
)
# 애플리케이션에 내장된 데이터베이스 사용
users = {}


@user_router.get("/users")
async def get_users()->dict:
    return users
# 사용자를 등록하기 전 데이터베이스에 비슷한 이메일이 존재하는지 확인
@user_router.post("/signup")
async def sign_new_user(data: User)->dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )
    users[data.email]=data
    return{
        "message" : 'User successfully registrerd!'
    }

# 로그인하려는 사용자가 데이터베이스에 존재하는지를 먼저 확인하고, 없으면 예외를 발생시킨다.
# 사용자가 존재하면 패스워드가 일치하는지 확인해서 성공 또는 실패 메시지를 반환한다.
@user_router.post("signin")
async def sign_user_in(user: UserSignIn)->dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )
    return{
        "message" : "User signed in successfulyy"
    }