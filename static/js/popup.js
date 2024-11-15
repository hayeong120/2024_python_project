let formData = null; // 전역 변수로 폼 데이터를 저장

document.querySelector('#borrow-form').addEventListener('submit', function (e) {
    e.preventDefault(); // 기본 제출 동작 방지

    // 폼 데이터를 저장
    formData = new FormData(this);

    // 첫 번째 팝업 열기
    openPopup();
});

// 첫 번째 팝업 열기
function openPopup() {
    document.querySelector('.popup').style.display = 'block';
}

// 첫 번째 팝업 닫기
function closePopup() {
    document.querySelector('.popup').style.display = 'none';
}

// 도서 반납 확인 버튼 클릭 시 호출되는 함수
function confirmReturn() {
    closePopup(); // 첫 번째 팝업 닫기

    // 두 번째 팝업 로직으로 이동하기 전에 fetch 호출
    fetchBorrowRequest();
}

// fetch 요청을 별도 함수로 분리
function fetchBorrowRequest() {
    fetch(document.querySelector('#borrow-form').action, {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const returnDate = data.return_date;
                document.getElementById('return-date').textContent = `반납일 : ${returnDate}`;
                openConfirmationPopup(); // 성공 팝업 표시
            } else {
                alert(`대출 예약에 실패했습니다: ${data.message || '알 수 없는 오류'}`);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            alert('대출 예약에 실패했습니다. 네트워크 문제일 수 있습니다.');
        });
}

// 두 번째 팝업 열기 (반납 완료 메시지)
function openConfirmationPopup() {
    document.querySelector('.confirmation-popup').style.display = 'block';

    // 2초 후에 두 번째 팝업 자동 닫기
    setTimeout(closeConfirmationPopup, 2000);
}

// 두 번째 팝업 닫기
function closeConfirmationPopup() {
    document.querySelector('.confirmation-popup').style.display = 'none';
}
