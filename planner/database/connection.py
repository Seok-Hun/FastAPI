# database 추상화와 설정에 사용
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
# 환경 파일(env_file)에서 읽어온다.
    DATABASE_URL: Optional[str] = None

# 데이터베이스 초기화
    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
# init_beanie() 메서드는 데이터베이스 클라이언트를 설정한다.
# SQLModel에서 생성한 몽고 엔진 버전과 문서 모델을 인수로 설정한다.
        await init_beanie(database=client.get_default_database(), document_models=[])

    class Config:
        env_file = ".env"