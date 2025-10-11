# backend/app/api/dependencies.py

from typing import Generator
from backend.app.db.session import SessionLocal

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db  # API 엔드포인트 함수에 db 세션을 전달(yield)
    finally:
        # API 요청 처리가 성공하든, 오류가 발생하든 상관없이
        # 마지막에는 항상 db.close()를 호출하여 세션을 닫음
        db.close()