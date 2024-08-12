# URL-shortner-project

URL 단축 서비스는 긴 URL을 짧게 단축하여 사용하고, 단축된 URL을 통해 원본 URL로 리디렉션하는 기능을 제공합니다.

![url-shortner-erd2](https://github.com/user-attachments/assets/27e298ba-64a7-44d3-bf94-4870d964c2f7)

## 개발 계획

#### 기술 스택
- 백엔드 : FastAPI
- DB : PostgreSQL, Redis
   - 관계형 데이터베이스인 PostgreSQL을 이용함으로써 URL과 관련된 모든 정보를 구조화된 방식으로 저장하고 비즈니스 로직에 따라서 복잡한 쿼리 및 트랜잭션 대응 가능
   - 또 자주 조회되는 URL을 Redis에 캐싱 하여 빠른 응답 속도를 보장하고 DB 부하를 줄일 수 있음
   - PostgreSQL을 이용함으로써 시간이 지난 통계 데이터를 TimescaleDB로 이전이 용이하다고 판단

#### 고려사항
- 단축 key 생성
    - id가 자동으로 1씩 증가하는 값으로 설정하면 다음에 쓸 URL이 무엇인지 알아낼 수 있는 보안 문제가 있을 수 있음
    - 따라서 URL 테이블의 id생성기를 따로 구현 후 저장하도록 설계

- 통계 데이터
    - 통계 데이터가 더욱 의미가 있으려면 날짜별로 기록해야 데이터를 더 정교하게 분석할 수 있다고 판단 (특정 기간 트래픽, 조회 수 추이 등등)
    - 따라서 통계 데이터를 위한 테이블 분리

- timezone=True ( created_at 필드 )
    - 전 세계 사용자들에게 서비스를 제공할 계획이 있는 경우 전역 시간 표준화 하는 것이 관리 용이

- 만료일 지났을 때 삭제 처리 방법
    - 설정한 만료일이 지난 key를 조회 시 is_active 필드를 false로 업데이트함으로써 soft-delete 처리
    - 통계 데이터는 연속성이 중요하다고 판단. 고객 이탈 분석 등 활용가치가 있을 수 있음


#### 실행 방법
🟦 아래 과정은 윈도우, 맥 둘다 정상 작동 확인 완료

1. repository를 다운받고 해당 위치로 이동 후 vscode열기

```
git clone https://github.com/msm9401/url-shortening.git

cd url-shortening

code .
```

<br>

2. 파이썬 가상환경 실행 후 requirements-dev.txt 설치

```
python -m venv venv

source venv/bin/activate

pip install -r requirements-dev.txt
```

<br>

3. docker-compose.dev.yml에 정의된 db실행

```
docker-compose -f docker-compose.dev.yml up -d --build
```
❗️❗️ 현재 테이블을 자동으로 생성해 주지 않습니다. db에 접속해서 CREATE TABLE ... 명령어로 정의된 모델에 대한 테이블을 직접 생성해야 합니다.<br>
❗️❗️ 테이블을 생성해 주지 않고 진행시 500에러

<br>

✅테이블 생성 과정 설명 추가합니다. (설명대로 진행해도 되지만 db에 접속하여 아래 2개의 sql문을 바로 복사하여 실행해도 무방)

```
# 파이참 - 파이썬 콘솔 열기
# vscode - "Jupyter: Create Interactive Window" 실행
# 아래 명령어들을 차례로 입력

from sqlalchemy.schema import CreateTable
from database.orm import Url, UrlStats
from database.connection import engine
```

```
print(CreateTable(Url.__table__).compile(engine))
```

```
print(CreateTable(UrlStats.__table__).compile(engine))
```

위 과정으로 아래 2개의 sql생성
```
CREATE TABLE url (
	id BIGINT NOT NULL,
	original_url VARCHAR NOT NULL,
	short_key VARCHAR(256) NOT NULL,
	expiration_date DATE,
	is_active BOOLEAN NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	PRIMARY KEY (id)
);
```

```
CREATE TABLE url_stats (
	id SERIAL NOT NULL,
	date DATE NOT NULL,
	access_count INTEGER NOT NULL,
	url_id BIGINT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(url_id) REFERENCES url (id)
);
```

db 접속 후 psql 실행
```
docker exec -it url-shortening-db bash

psql --username shortner --dbname shortner
```

위에서 생성된 2개의 sql문으로 테이블 생성 후 진행

<br>

4. uvicorn 실행 후 swagger이동

```
uvicorn main:app --reload
```
swagger 이동 : http://127.0.0.1:8000/docs

![FastAPI-SwaggerUI](https://github.com/user-attachments/assets/e4e1e9e3-6d3c-43fb-bbf2-b701cfafe9cf)

#### URL 단축 흐름도
❗️❗️ 상세한 로직은 코드를 참고해 주세요
![url-shortner-flow](https://github.com/user-attachments/assets/e50f0226-ac4f-49ac-b22e-570efa62c765)


#### URL 리디렉션 흐름도
❗️❗️ 상세한 로직은 코드를 참고해 주세요
![url-return](https://github.com/user-attachments/assets/c1bc211f-bec7-40d8-9fcb-3d5babcb10d4)