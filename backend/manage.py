import typer
import uvicorn
import mimetypes
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from backend.app.core.utils import register
from backend.app.core.config import STATIC_DIR
from backend.app.management.commands import seed_memes

# Typer CLI 애플리케이션 (관리자 명령어용)
cli_app = typer.Typer()

# FastAPI Web 애플리케이션 (API 서버용)
api_app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
api_app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)

# --- FastAPI 웹 앱(`api_app`)에 대한 설정 ---
mimetypes.init()
mimetypes.add_type("application/javascript", ".js", strict=True)

api_app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

register(api_app, 'backend.app.routes.main')

# --- Typer CLI 앱(`cli_app`)에 명령어 등록 ---
cli_app.command("seed-memes")(seed_memes.main)

@cli_app.command("run-server")
def run_server(
    host: str = typer.Option("127.0.0.1", help="Host IP to run the server on."),
    port: int = typer.Option(8000, help="Port to run the server on."),
    reload: bool = typer.Option(True, help="Enable auto-reloading.")
):
    """FastAPI 개발 서버 실행"""
    typer.echo(f"Starting server on http://{host}:{port}")
    uvicorn.run(
        "manage:api_app",  # 실행할 앱: "파일이름:FastAPI인스턴스이름"
        host=host,
        port=port,
        reload=reload,
        factory=True # factory=True를 사용하려면 create_app 함수가 필요 -> 아래에서 수정.
    )

# `manage.py`가 직접 실행될 때 CLI 앱을 실행하도록 설정
if __name__ == "__main__":
    cli_app()

# uvicorn이 --factory 옵션으로 이 파일을 로드할 때 사용할 함수
def create_app():
    return api_app