-- --- 밈 컨텐츠 관리 테이블 ---

CREATE TABLE memes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    image_url VARCHAR(2048),
    year SMALLINT,
    month SMALLINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- memes와 tags를 연결하는 중간 테이블 (다대다 관계)
CREATE TABLE meme_tags (
    meme_id INTEGER NOT NULL REFERENCES memes(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (meme_id, tag_id) -- 두 컬럼을 묶어서 기본 키로 설정
);


-- --- 퀴즈 컨텐츠 관리 테이블 ---

CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    image_url VARCHAR(2048),
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE
);


-- --- 사용자 응시 결과 관리 테이블 ---

CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    final_score INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE user_answers (
    id SERIAL PRIMARY KEY,
    quiz_attempt_id INTEGER NOT NULL REFERENCES quiz_attempts(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    selected_choice_id INTEGER NOT NULL REFERENCES choices(id) ON DELETE CASCADE
);

-- 각 테이블에 대한 주석 추가 (선택 사항)
COMMENT ON TABLE memes IS '밈 컨텐츠 정보';
COMMENT ON TABLE tags IS '밈 관련 태그';
COMMENT ON TABLE quizzes IS '밈 지식 퀴즈 정보';
COMMENT ON TABLE questions IS '퀴즈에 포함된 문제';
COMMENT ON TABLE choices IS '문제에 대한 선택지';
COMMENT ON TABLE quiz_attempts IS '사용자의 퀴즈 응시 기록';
COMMENT ON TABLE user_answers IS '사용자의 개별 문제 답변 기록';