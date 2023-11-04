# database 추상화와 설정에 사용
from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

# 데이터베이스 파일의 위치(없는 경우 생성)
database_file = "planner.db"
# 연결 문자열
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False}
# SQL 데이터베이스의 인스턴스
# echo를 True로 하여 SQL 명령이 화면에 출력된다.
engine_url = create_engine(database_connection_string, echo=True, connect_args=connect_args)

# SQLModel을 사용해 데이터베이스와 테이블 생성
def conn():
    SQLModel.metadata.create_all(engine_url)

# 데이터베이스 세션을 애플리케이션 내에서 유지
def get_session():
    with Session(engine_url) as session:
        yield session