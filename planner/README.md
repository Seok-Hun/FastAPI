# 이벤트 플래너 애플리케이션
## 개요
### 구조화 사용
- **구조화** : 애플리케이션 컴포넌트를 형식(모듈)에 맞춰 정리하는 것
    - **모듈화(modular)** : 애플리케이션 코드와 콘텐츠의 가독성을 높여준다.
    - 적절히 구조화된 애플리케이션은 개발 속도와 디버깅 속도를 빠르게 하고 전체적인 생산성도 향상시킨다.
### 애플리케이션 설명
- 등록된 사용자는 이벤트를 추가, 변경, 삭제할 수 있으며 애플리케이션이 자동으로 만든 이벤트 페이지에서 생성된 이벤트 확인 가능
- 등록된 사용자와 이벤트는 모두 고유한 ID를 가짐
    - 사용자와 이벤트가 주복되는 것 방지
## 구현
### 모델 구현
1. 이벤트 모델과 사용자 모델을 정의한다.
- 이 모델들은 데이터가 어떤 방식으로 입력 및 저장되고 애플리케이션에 표현되는지를 정의한다.
- 모델 예시
    - 사용자
        - Email
        - Password
        - Username
        - Events
    - 이벤트
        - Title
        - Image
        - Description
        - Tags
        - Location
- 각 사용자는 Events 필드를 가지며 여러 이벤트를 저장할 수 있다.
2. 이벤트 모델(Event)을 models 폴더의 events.py에 정의
    1. Event 클래스 안에 Config 서브 클래스 추가
3. 사용자 모델(User)을 models 폴더의 users.py 파일에 정의
    1. User 클래스 안에 Config 서브 클래스 추가
    2. 사용자 로그인 모델(UserSignIn)을 만든다.
### 라우트 구현
API의  라우트 시스템 구현<br/>
- 사용자 라우트 시스템 설계
    - 사용자 라우트는 로그인, 로그아웃, 등록으로 구성
    - 인증을 완료한 사용자는 이벤트 생성, 변경, 삭제 가능
    - 인증을 거치지 않은 사용자는 이벤트 확인만 가능
    - 라우트
        - 사용자: /user
            - /signup
            - /signin
            - /signout
        - 이벤트: /event
            - 생성 : /new
            - 조회 : /, /{id}
            - 변경 : /{id}
            - 삭제 : /{id}
#### 사용자 라우트
routes 폴더의 users.py에 사용자 라우트 정의
1. 등록(/signup) 라우트 정의
2. 로그인(/signin) 라우트 정의
3. min.py에 라우트 등록
    1. 라이브러리와 사용자 라우트 정의 임포트
    2. FastAPI()인스턴스를 만들고 정의한 라우트 등록
    3. uvicorn.run() 메소드로 8000번 포트에서 애플리케이션을 실행하도록 설정
### 이벤트 라우트
routes 폴더의 events.py에 이벤트 라우트 정의
1. 의존 라이브러리 import
2. 이벤트 추출 라우트 정의
3. 이벤트 생성 및 삭제 라우트 정의
4. main.py에 이벤트 라우트 추가
# 데이터베이스 연결
## 개요
### 사용 데이터베이스 : MongoDB
## SQLModel 설정

>SQL과 NoSQL 데이터베이스를 모두 구현해야 하므로 새로운 Git 브랜치 작성

SQL 데이터베이스와 이벤트 플래너 애플리케이션을 연동하려면 먼저 **SQLModel 라이브러리**를 설치해야 한다.

>[!Note]
>### SQLModel
>- FastAPI 개발자가 만든 라이브러리
>- pydanic과 SQLAlchemy를 기반으로 한다.
>- SQLAlchemy 엔진을 사용해 데이터베이스에 연결한다.

### SQLModel 구조와 기능
#### 테이블
데이터베이스에 저장된 데이터를 가지고 있는 객체<br>
Column과 Row로 구성되며 구조에 맞게 데이터가 저장된다.<br>
##### SQLModel로 테이블 생성
- 테이블 모델 클래스를 먼저 정의해야 한다.
    - pydanic 모델처럼 테이블을 정의 가능
    - SQLModel 서브 클래스로 정의 가능
        - 클래스 정의는 table이라는 설정 변수를 가진다.
        - 이 변수로 해당 클래스가 SQLModel 테이블임을 인식한다.
- 모델 클래스 안에 정의된 변수는 따로 지정하지 않으면 기본 필드로 설정된다.
    - 필드의 특성을 지정하고 싶으면 Field() 함수 사용
- 이벤트 테이블 정의 예시
    ```python
    class Event(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        image: str
        description: str
        location: str
        tags: List[str]
    ```
    - id만 필드로 정의되고 나머지는 Column으로 정의된다.
        - 필드는 Field() 객체를 사용해서 정의했다.
    - id 필드는 테이블의 기본키(PK, Primary key)로도 사용된다.
#### Row
데이터베이스 테이블로 전달된 데이터는 특정 Column 아래에 있는 Row에 저장된다.
- Row에 데이터 추가
    - 테이블의 인스턴스를 만든 후 인스턴스의 변수에 원하는 데이터를 할당한다.
- Row 데이터 추가 예시 - 하나의 이벤트 데이터를 이벤트 테이블에 추가하기 위해 이벤트 모델의 인서턴스 정의
    ```python
    new_event = Event(
        title="Book Launch",
        image="src/fastapi.png",
        description="The book launch event will be held at Packt HQ, Packt city",
        location="Google Meet",
        tags=["packt","book"])
    ```
#### Session
- 코드와 데이터베이스 사이에서 이루어지는 처리를 관리하는 객체
    - 주로 특정 처리를 데이터베이스에 적용하기 위해 사용된다.
- Session 클래스는 SQL 엔진의 인스턴스를 인수로 사용한다.
- Row에 데이터를 추가하면 Session 클래스를 사용해서 데이터베이스 트랜잭션을 만든다.
    - 예시
        ```python
        with Session(engine) as session:
            session.add(new_event)
            session.commit()
        ```
- Session 클래스의 메소드 일부
    - add()
        - 처리 대기중인 데이터베이스 객체를 메모리에 추가한다.
        - 예시 코드를 활용한 설명
            - new_event 객체는 세션 메모리에 추가되고 commit() 메소드에 의해 데이터베이스에 commit(등록)될 때까지 대기했다.
    - commit()
        - 현재 세션에 있는 트랜잭션을 모두 정리한다.
    - get()
        - 데이터베이스에서 단일 Row를 추출한다.
        - 모델과 문서 ID를 인수로 사용한다.
## 데이터베이스 생성
SQLAlchemy 엔진을 이용해 데이터베이스를 연결한다.
### SQLAlchemy 엔진
- create_engine() 메소드를 사용해 만들 수 있다.
    - SQLModel 라이브러리에서 import 가능하다.
    - 단, create_engine() 메소드만으로는 데이터베이스 파일을 만들 수 없다.
        - SQLModel.metadata.create_all(engine) 메소드를 사용해 create_engine() 메소드의 인스턴스를 호출해야 한다.
            ```python
            database_file="database.db"
            engine=create_engine(database_file, echo=True)
            SQLModel.metadata.create_all(engine)
            ```
### create_engine()
- 데이터 베이스 URL을 인수로 사용
- echo를 선택적 인수로 지정 가능
    - True로 설정하면 실행된 SQL 명령을 출력한다.
- 데이터베이스뿐만 아니라 테이블도 생성 가능
    - 데이터베이스 연결 파일(connection.py)에서 테이블 파일을 import 해야 한다.
## 구현
### 데이터베이스 연결
1. database 폴더에 connection.py 파일 생성
- 해당 파일에서 데이터베이스 연결을 위한 데이터를 설정한다.
2. models/events.py에 정의한 이벤트 모델 클래스(Evnet)를 변경
- SQLModel의 테이블 클래스를 사용하도록 한다.
- 기존 모델 클래스를 SQL 테이블 클래스로 변경
3. UPDATE 처리의 Body유형으로 사용할 SQLModel 클래스 추가
4. connection.py에 데이터베이스 및 테이블 생성을 위한 설정 작성
5. main.py에 conn 추가
### 이벤트 생성
CRUD 처리 라우트 변경
1. routes/events.py를 변경해서 이벤트 테이블 클래스와 get_session() 함수 import
- get_session() 함수로 라우트가 세션 객체에 접근 가능
2. 신규 이벤트 생성 담당 라우트에 get_session 추가