# backend/app/routes/main.py
from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List

from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from backend.app.api import dependencies
from backend.app.db.models import Meme # Tag 모델은 Meme.tags를 통해 접근하므로 직접 임포트 안해도 됨

from backend.app.core.config import TEMPLATES_DIR 

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/", response_class=HTMLResponse)
def main(request: Request, db: Session = Depends(dependencies.get_db)):

    # order_by(Meme.id.desc()): 최신 밈이 위로 오도록 id 역순으로 정렬
    memes_from_db = db.query(Meme)\
                      .filter(Meme.region == '국내')\
                      .order_by(Meme.id.desc())\
                      .limit(4)\
                      .all()

    meam_list = []
    for meme in memes_from_db:
        meme_dict = {
            "id": meme.id,
            "title": meme.title,
            # meme.tags relationship을 통해 Tag 객체 리스트를 가져오고, 각 tag의 name만 추출
            "tags": [tag.name for tag in meme.tags],
            # 이미지가 없는 경우(None)를 대비하여 기본 이미지 경로 제공
            "image_url": meme.image_url if meme.image_url else "/static/assets/images/default-image.png"
        }
        meam_list.append(meme_dict)

    today_date = datetime.now().strftime("%Y년 %m월 %d일")

    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request, 
            "meam_list": meam_list, 
            "today_date": today_date
            } 
    )

@router.get("/quiz", response_class=HTMLResponse)
def meme_test(request: Request):
    return templates.TemplateResponse(
        name="meme_test.html",
         context={
            "request": request
        }
    )

correct_answers = [
    '무야호', '중요한 것은 꺾이지 않는 마음', '너 T야?', '삐끼삐끼', '슬릭백',
    '개웃겨서 도티낳음', '그 잡채', '사과해', '군침이 싹 도노', '어쩔티비',
    '알잘딱깔센', '오히려 좋아', '가보자고', '관짝춤', '멋지다 연진아'
]

# 등급 정의
tiers = [
    {"score": 0, "name": "밈 베이비", "icon": "🍼", "desc": "혹시 인터넷 오늘 개통하셨나요? 괜찮아요, 이제부터 알아가면 되죠!"},
    {"score": 4, "name": "밈 새싹", "icon": "🌱", "desc": "요즘 유행은 좀 아시는군요! 성장 가능성이 무한합니다."},
    {"score": 8, "name": "밈 고수", "icon": "😎", "desc": "친구들 사이에서 '밈잘알' 소리 좀 듣겠는데요? 꽤 높은 수준입니다."},
    {"score": 12, "name": "밈 장인", "icon": "💎", "desc": "상위 1%의 밈센스를 보유한 당신! 모든 상황을 밈으로 표현할 수 있는 수준이에요."},
    {"score": 15, "name": "밈 화석", "icon": "🗿", "desc": "당신은 살아있는 인터넷의 역사 그 자체입니다. 존경스럽습니다."}
]

class UserAnswers(BaseModel):
    answers: List[str]

@router.post("/submit")
async def submit_quiz(request: Request, user_answers: UserAnswers):
    """
    사용자 답안을 받아 채점하고, 결과를 세션에 저장합니다.
    """
    score = 0
    for i, user_answer in enumerate(user_answers.answers):
        # 간단한 채점 로직: 정답에 사용자 답이 포함되면 정답 처리
        if user_answer and user_answer.lower() in correct_answers[i].lower():
            score += 1
    
    # 점수에 맞는 등급 찾기
    user_tier = tiers[0]
    for tier in reversed(tiers):
        if score >= tier["score"]:
            user_tier = tier
            break
            
    # 채점 결과를 세션에 저장
    request.session['quiz_result'] = {
        "score": score,
        "total_questions": len(correct_answers),
        "tier_name": user_tier["name"],
        "tier_icon": user_tier["icon"],
        "tier_description": user_tier["desc"],
    }

    return JSONResponse({"redirect_url": "/result"})


@router.get("/result")
async def show_result(request: Request):
    """
    세션에서 결과 데이터를 읽어 result.html 템플릿을 렌더링합니다.
    """
    result_data = request.session.get('quiz_result')

    # 만약 세션에 결과가 없으면 (예: URL로 바로 접속 시도) 퀴즈 시작 페이지로 리다이렉트
    if not result_data:
        # 이 부분은 실제 퀴즈 시작 페이지의 URL로 변경해야 합니다.
        return templates.TemplateResponse("quiz.html", {"request": request})

    return templates.TemplateResponse("result.html", {"request": request, **result_data})