import os
import pandas as pd
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from backend.app.core.config import TEMPLATES_DIR 


router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/", response_class=HTMLResponse)
def main(request: Request):

    meam_data_from_db = [
        {"id": 1, "title": "삐끼삐끼 춤", "tags": ["댄스챌린지", "중독성"], "image_url": "/static/assets/images/meam1.jpg"},
        {"id": 2, "title": "창밖 (다 해줬잖아)", "tags": ["정상훈", "리액션"], "image_url": None}, # 이미지가 없는 경우
        {"id": 3, "title": "형이랑 내기할래?", "tags": ["유행어", "챌린지"], "image_url": "/static/assets/images/meam3.jpg"},
        {"id": 4, "title": "류정란 챌린지", "tags": ["코미디", "상황극"], "image_url": "/static/assets/images/meam4.jpg"},
    ]

    return templates.TemplateResponse(
        name="main.html",
        context={"request": request, "meam_list": meam_data_from_db} 
    )
