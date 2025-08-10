from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

# 모든 모델이 상속받을 기본 클래스
Base = declarative_base()

# --------------------------------------------------------------------
# 밈(Meme)과 태그(Tag)를 위한 다대다(Many-to-Many) 관계를 정의하는
# 중간 테이블(Association Table)
# --------------------------------------------------------------------
meme_tags_table = Table(
    "meme_tags",
    Base.metadata,
    Column("meme_id", Integer, ForeignKey("memes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

# --------------------------------------------------------------------
# 밈 컨텐츠 관리 모델
# --------------------------------------------------------------------

class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    image_url = Column(String(2048))
    year = Column(Integer)
    month = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Meme과 Tag의 관계 설정 (다대다)
    tags = relationship("Tag", secondary=meme_tags_table, back_populates="memes")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    
    # Tag와 Meme의 관계 설정 (다대다)
    memes = relationship("Meme", secondary=meme_tags_table, back_populates="tags")


# --------------------------------------------------------------------
# 퀴즈 컨텐츠 및 결과 관리 모델
# --------------------------------------------------------------------

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    # Quiz와 Question의 관계 설정 (일대다)
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    # Quiz와 QuizAttempt의 관계 설정 (일대다)
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    image_url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    # Question과 Quiz의 관계 설정
    quiz = relationship("Quiz", back_populates="questions")
    # Question과 Choice의 관계 설정 (일대다)
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")


class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)

    # Choice와 Question의 관계 설정
    question = relationship("Question", back_populates="choices")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    final_score = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    completed_at = Column(TIMESTAMP(timezone=True))

    # QuizAttempt와 Quiz의 관계 설정
    quiz = relationship("Quiz", back_populates="attempts")
    # QuizAttempt와 UserAnswer의 관계 설정 (일대다)
    answers = relationship("UserAnswer", back_populates="attempt", cascade="all, delete-orphan")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    selected_choice_id = Column(Integer, ForeignKey("choices.id", ondelete="CASCADE"), nullable=False)

    # UserAnswer와 QuizAttempt의 관계 설정
    attempt = relationship("QuizAttempt", back_populates="answers")
