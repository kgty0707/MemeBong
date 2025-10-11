# backend/app/management/commands/seed_memes.py

import json
import re
from pathlib import Path

import typer  # Typer 임포트
from sqlalchemy.orm import Session

from backend.app.db.session import SessionLocal
from backend.app.db.models import Meme, MemePopularity


def main(
    file_path: Path = typer.Argument(
        ...,  # '...'는 이 인자가 필수임을 의미
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="데이터를 로드할 JSON 파일 경로입니다."
    )
):
    """
    JSON 파일을 읽어 Meme 데이터를 데이터베이스에 시딩(seeding)합니다.
    """
    typer.echo(f"'{file_path}' 파일에서 데이터 로드를 시작합니다...")

    db: Session = SessionLocal()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        new_meme_count = 0
        new_popularity_count = 0
        
        for item in data:
            title = item.get('title')
            if not title:
                continue

            # 밈(Meme)이 DB에 이미 있는지 확인하고, 없으면 새로 생성
            meme = db.query(Meme).filter(Meme.title == title).first()
            if not meme:
                meme = Meme(
                    title=title,
                    region=item.get('region')
                )
                db.add(meme)
                # db.commit()  # commit을 해야 meme.id가 확정
                db.flush()
                db.refresh(meme)
                new_meme_count += 1
                typer.secho(f"✅ 새로운 밈 생성: '{title}' (ID: {meme.id})", fg=typer.colors.GREEN)
            
            elif not meme.region and item.get('region'):
                meme.region = item.get('region')
                typer.secho(f"🔄 밈 정보 업데이트: '{title}'에 지역 '{meme.region}' 추가", fg=typer.colors.YELLOW)
            
            # 유행 시기(MemePopularity)
            year_str = item.get('year_sub', '')
            year_match = re.search(r'\d{4}', year_str)
            year = int(year_match.group(0)) if year_match else None

            month_str = item.get('month', '')
            month_match = re.search(r'\d+', month_str)
            month = int(month_match.group(0)) if month_match else None

            if year:
                # 동일한 밈에 동일한 연/월 데이터가 있는지 확인하여 중복 방지
                exists = db.query(MemePopularity).filter_by(meme_id=meme.id, year=year, month=month).first()
                if not exists:
                    popularity = MemePopularity(meme_id=meme.id, year=year, month=month)
                    db.add(popularity)
                    new_popularity_count += 1

        db.commit() # 루프가 끝난 후 모든 유행 시기 정보를 한 번에 커밋
        typer.secho(
            f"\n🎉 성공! 새로운 밈 {new_meme_count}개, 유행 시기 정보 {new_popularity_count}개가 추가되었습니다.",
            fg=typer.colors.BRIGHT_BLUE
        )

    except Exception as e:
        db.rollback()
        typer.secho(f"오류가 발생하여 모든 변경사항을 롤백: {e}", fg=typer.colors.RED)
    finally:
        db.close()
        typer.echo("데이터베이스 close.")