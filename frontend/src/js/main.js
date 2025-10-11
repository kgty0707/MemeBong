document.addEventListener('DOMContentLoaded', () => {

    const startScreen = document.getElementById('start-screen');
    const quizScreen = document.getElementById('quiz-screen');
    const startButton = document.getElementById('start-button');
    
    const progressBar = document.getElementById('progress-bar');
    const questionCounter = document.getElementById('question-counter');
    const imageContainer = document.getElementById('image-container');
    const answerInput = document.getElementById('meme-answer');
    const submitButton = document.getElementById('submit-button');
    const nextButton = document.getElementById('next-button');

    const quizData = [
        { image_url: '/static/images/meme_1.jpg', answer: '무야호' },
        { image_url: '/static/images/meme_2.jpg', answer: '중요한 것은 꺾이지 않는 마음' },
        { image_url: '/static/images/meme_3.jpg', answer: '너 T야?' },
        { image_url: '/static/images/meme_4.jpg', answer: '삐끼삐끼' },
        { image_url: '/static/images/meme_5.jpg', answer: '슬릭백' },
        { image_url: '/static/images/meme_6.jpg', answer: '개웃겨서 도티낳음' },
        { image_url: '/static/images/meme_7.jpg', answer: '그 잡채' },
        { image_url: '/static/images/meme_8.jpg', answer: '사과해' },
        { image_url: '/static/images/meme_9.jpg', answer: '군침이 싹 도노' },
        { image_url: '/static/images/meme_10.jpg', answer: '어쩔티비' },
        { image_url: '/static/images/meme_11.jpg', answer: '알잘딱깔센' },
        { image_url: '/static/images/meme_12.jpg', answer: '오히려 좋아' },
        { image_url: '/static/images/meme_13.jpg', answer: '가보자고' },
        { image_url: '/static/images/meme_14.jpg', answer: '관짝춤' },
        { image_url: '/static/images/meme_15.jpg', answer: '멋지다 연진아' },
    ];

    let currentQuestionIndex = 0;
    const userAnswers = [];

    function startQuiz() {
        startScreen.style.display = 'none';
        quizScreen.style.display = 'block';
        loadQuestion(currentQuestionIndex);
    }

    function loadQuestion(index) {
        if (index >= quizData.length) {
            endQuiz();
            return;
        }

        const question = quizData[index];
        imageContainer.innerHTML = `<img src="${question.image_url}" class="img-fluid rounded" alt="밈 이미지">`;
        questionCounter.textContent = `${index + 1} / ${quizData.length}`;
        const progress = ((index + 1) / quizData.length) * 100;
        progressBar.style.width = `${progress}%`;
        answerInput.value = '';
        answerInput.focus();
    }
    
    function handleNextQuestion() {
        const answer = answerInput.value.trim();
        userAnswers.push(answer);
        currentQuestionIndex++;
        loadQuestion(currentQuestionIndex);
    }

    async function endQuiz() {
    // 퀴즈 화면에 로딩 표시
        quizScreen.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <h2 class="fw-bold mt-4">결과를 분석하고 있습니다...</h2>
            </div>
        `;

        try {
            const response = await fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ answers: userAnswers }),
            });

            if (!response.ok) {
                throw new Error('서버에 결과를 전송하는데 실패했습니다.');
            }

            const result = await response.json();

            // 서버가 알려준 결과 페이지 URL로 이동
            if (result.redirect_url) {
                window.location.href = result.redirect_url;
            }

        } catch (error) {
            console.error('Error:', error);
            alert('결과를 처리하는 중 오류가 발생했습니다.');
        }
    }


    startButton.addEventListener('click', startQuiz);
    submitButton.addEventListener('click', handleNextQuestion);
    nextButton.addEventListener('click', handleNextQuestion);

    answerInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            handleNextQuestion();
        }
    });
});