let formData = null; // 전역 변수로 폼 데이터를 저장

// 도서 대출 폼 제출 이벤트 리스너
document.querySelector('#borrow-form').addEventListener('submit', function (e) {
    e.preventDefault(); // 기본 제출 동작 방지

    // 폼 데이터를 저장
    formData = new FormData(this);

    // 첫 번째 팝업 열기
    openBorrowPopup();
});

// 대출 팝업 열기
function openBorrowPopup() {
    document.querySelector('.popup').style.display = 'block';
}

// 대출 팝업 닫기
function closeBorrowPopup() {
    document.querySelector('.popup').style.display = 'none';
}

// 대출 확인 버튼 클릭 시 호출되는 함수
function confirmBorrow() {
    closeBorrowPopup(); // 첫 번째 팝업 닫기

    // 서버에 대출 요청 전송
    fetchBorrowRequest();
}

// 서버에 대출 요청
function fetchBorrowRequest() {
    console.log('Sending data:', Object.fromEntries(formData.entries())); // 폼 데이터 확인

    fetch(document.querySelector('#borrow-form').action, {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                console.error('Network response was not ok', response.status);
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data); // 서버 응답 확인

            if (data.success) {
                const returnDate = data.return_date;
                document.getElementById('return-date').textContent = `반납일 : ${returnDate}`;
                openBorrowConfirmationPopup();
            } else if (data.message && data.message.includes('대출 한도 초과')) {
                openBorrowLimitPopup();
            } else {
                alert('대출 예약에 실패했습니다: ' + (data.message || '알 수 없는 오류'));
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            alert('대출 예약에 실패했습니다. 네트워크 문제일 수 있습니다.');
        });
}

// 대출 성공 팝업 열기
function openBorrowConfirmationPopup() {
    document.querySelector('.confirmation-popup').style.display = 'block';

    // 2초 후에 팝업 자동 닫기
    setTimeout(closeBorrowConfirmationPopup, 2000);
}

// 대출 성공 팝업 닫기
function closeBorrowConfirmationPopup() {
    document.querySelector('.confirmation-popup').style.display = 'none';
}

// 대출 초과 팝업 열기
function openBorrowLimitPopup() {
    document.querySelector('.limit-popup').style.display = 'block';

    // 2초 후에 두 번째 팝업 자동 닫기
    setTimeout(closeBorrowLimitPopup, 2000);
}

// 대출 초과 팝업 닫기
function closeBorrowLimitPopup() {
    document.querySelector('.limit-popup').style.display = 'none';
}
