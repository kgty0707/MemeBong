import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,  # autocommit=False: 커밋은 수동으로 관리
    autoflush=False,   # autoflush=False: 필요한 경우에만 DB에 데이터를 반영(flush)
    bind=engine        # bind=engine: 이 세션 팩토리가 사용할 엔진을 지정
)