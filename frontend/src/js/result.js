document.addEventListener('DOMContentLoaded', () => {
    // '결과 카드 이미지 다운로드' 버튼 기능
    const downloadBtn = document.getElementById('download-button');
    downloadBtn.addEventListener('click', () => {
        // .card 요소를 이미지로 캡처
        html2canvas(document.querySelector(".card")).then(canvas => {
            // 캔버스를 이미지 URL로 변환
            const imgURL = canvas.toDataURL("image/png");
            
            // 다운로드 링크 생성 및 클릭
            const link = document.createElement('a');
            link.href = imgURL;
            link.download = 'my_meme_result.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    });

    // '친구에게 공유하기' 버튼 기능 (현재 URL 복사)
    const shareBtn = document.getElementById('share-button');
    shareBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(window.location.href).then(() => {
            alert('결과 링크가 복사되었습니다!');
        }).catch(err => {
            console.error('클립보드 복사 실패:', err);
        });
    });
});