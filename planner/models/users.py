# 사용자 처리용 모델을 정의
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event
from beanie import Document, Link

# 사용자 모델은 3개의 필드를 가진다.(내부 데이터 활용)
'''
class User(BaseModel):
    # 사용자 이메일
    email: EmailStr
    # 사요자 패스워드
    password: str
    # 사용자 이름
    username: str
    # 해당 사용자가 생성한 이벤트. 처음에는 비어 있다.
    events: Optional[List[Event]]=None

    # Config 서브 클래스 : 문서화할 때 샘플 데이터를 보여주기 위한 용도
    # 이벤트의 샘플 데이터를 정의한다.
    # 우리가 API를 통해 신규 이벤트를 생성할 때 참고할 수 있다.
    class Config:
        schema_extra = {
            "example":{
                "email" : "fastapi@packt.com",
                "username":"strong!!",
                "events": []
            }
        }
'''

# 사용자 모델은 3개의 필드를 가진다.(데이터베이스(mongodb) 활용)

# 사용자 로그인 모델
class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example":{
                "email" : "fastapi@packt.com",
                "username":"strong!!",
                "events": []
            }
        }
        