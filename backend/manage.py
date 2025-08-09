from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.app.core.utils import register
from backend.app.core.config import STATIC_DIR 
import mimetypes

def create_app():
    app = FastAPI()

    mimetypes.init()
    mimetypes.add_type("application/javascript", ".js", strict=True)

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    register(app, 'backend.app.routes.main')

    return app

if __name__ == '__main__':
    import uvicorn
    # uvicorn backend.manage:create_app --factory --reload
    uvicorn.run("manage:create_app", host="localhost", port=8000, reload=True, factory=True)
