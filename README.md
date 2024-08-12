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

#### URL 단축 흐름도
![url-shortner-flow](https://github.com/user-attachments/assets/e50f0226-ac4f-49ac-b22e-570efa62c765)


#### URL 리디렉션 흐름도
![url-return](https://github.com/user-attachments/assets/c1bc211f-bec7-40d8-9fcb-3d5babcb10d4)