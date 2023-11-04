# 이벤트 처리용 모델을 정의
from pydantic import BaseModel
from typing import List

# 이벤트 모델은 6개의 필드를 가진다.
class Event(BaseModel):
    # id : 자동 생성되는 고유 식별자
    id: int
    # title : 이벤트 타이틀
    title: str
    # image : 이벤트 이미지 배너의 링크
    image: str
    # description : 이벤트 설명
    description: str
    # tags : 그룹화를 위한 이벤트 태그
    tags: List
    # location : 이벤트 위치
    location: str
    
    # Config 서브 클래스 : 문서화할 때 샘플 데이터를 보여주기 위한 용도
    # 이벤트의 샘플 데이터를 정의한다.
    # 우리가 API를 통해 신규 이벤트를 생성할 때 참고할 수 있다.
    class Config:
        schema_extra = {
            "example":{
                "title":"FastAPI Book Launch",
                "image":"https://linktomyimage.com/image.png",
                "description":"We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags":["python","fastapi","book","launch"],
                "location":"Google Meet"
            }
        }