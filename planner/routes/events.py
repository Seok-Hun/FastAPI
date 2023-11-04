# 이벤트 생성, 변경, 삭제 등의 처리를 위한 라우팅
# Depends 클래스 : FastAPI 애플리케이션에서 의존성 주입을 담당
#  함수를 인수로 사용하거나 함수 인수를 라우트에 전달할 수 있게 해서 어떤 처리가 실행되든지 필요한 의존성을 확보해준다.
from fastapi import APIRouter, Body, HTTPException, status, Depends,Request
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List
from sqlmodel import select

event_router = APIRouter(
    tags=["Events"]
)

events = []

'''
# 내부 데이터를 사용하는 모든 이벤트 추출 라우터
@event_router.get("/",response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events
'''

# 데이터베이스를 사용하는 모든 이벤트 추출 라우터
@event_router.get("/",response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session))->List[Event]:
    statement = select(Event)
    events=session.exec(statement).all()
    return events
'''
# 내부 데이터를 사용하는 특정 ID의 이벤트만 추출하는 라우터
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id:int)->Event:
    for event in events:
        if event.id == id:
            return event
# 해당 ID의 이벤트가 없으면 404 예외 발생
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
'''

# 데이터베이스를 사용하는 특정 ID의 이벤트만 추출하는 라우터
@event_router.get("{/id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session))->Event:
    event=session.get(Event,id)
    if event:
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

# 내부 데이털를 사용하는 이벤트 생성 라우터
'''
@event_router.post("/new")
async def create_event(body: Event=Body(...))->dict:
    events.append(body)
    return{
        "message" : "Event created successfully."
    }
'''

# 데이터베이스를 사용하는 이벤트 생성 라우터
@event_router.post("/new")
# 데이터베이스 처리에 필요한 세션 객체가 get_session() 함수에 의존하도록 설정
async def create_event(new_event:Event, session=Depends(get_session))->dict:
    print(new_event)
# 데이터(event)를 세션에 추가
    session.add(new_event)
# 데이터베이스에 commit(등록)
    session.commit()
# 세션 업데이트
    session.refresh(new_event)
    return{
        "message" : "Event created successfully."
    }

# 내부 데이터를 활용하는 특정 이벤트 삭제 라우터
'''
@event_router.delete("/{id}")
async def delete_event(id: int)->dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return{
                "message" : "Event deleted successfully."
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
'''

# 데이터베이스를 활용하는 특정 이벤트 삭제 라우터
@event_router.delete("/delete/{id}")
async def delete_event(id: int, session=Depends(get_session))->dict:
    event = session.get(Event,id)
    if event:
        session.delete(event)
        session.commit()
        return{
            "message": "Event deleted successfully."
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

# 내부 데이터를 활용하는 모든 이벤트 삭제 라우터
'''
@event_router.delete("/")
async def delete_al_events()->dict:
    events.clear()
    return{
        "message":"Events deleted successfully."
    }
'''

# 데이터베이스를 사용하는 이벤트 변경 라우터
@event_router.put("/edit/{id}", response_model=Event)
async def update_evetn(id: int, new_data: EventUpdate, session=Depends(get_session))->Event:
    event = session.get(Event, id)
# 이벤트를 변경하기 전에 이벤트가 존재하는지 먼저 확인
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)

        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
