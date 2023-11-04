# 이벤트 생성, 변경, 삭제 등의 처리를 위한 라우팅
from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event
from typing import List

event_router = APIRouter(
    tags=["Events"]
)

events = []

# 모든 이벤트 추출
@event_router.get("/",response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events

# 특정 ID의 이벤트만 추출
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

# 이벤트 생성 라우터
@event_router.post("/new")
async def create_event(body: Event=Body(...))->dict:
    events.append(body)
    return{
        "message" : "Event created successfully."
    }

# 특정 이벤트 삭제 라우터
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

# 모든 이벤트 삭제 라우터
@event_router.delete("/")
async def delete_al_events()->dict:
    events.clear()
    return{
        "message":"Events deleted successfully."
    }