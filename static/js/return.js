let bookId = null; // 전역 변수로 반납할 도서 ID 저장

// 도서 반납 팝업 열기
function openReturnPopup(button) {
    bookId = button.dataset.bookId; // 버튼의 data-book-id 속성에서 값 읽기

    if (!bookId) {
        console.error("Invalid book ID"); // 디버깅 로그
        alert("도서 ID를 가져올 수 없습니다."); // 오류 처리
        return;
    }

    const popup = document.querySelector('.popup.return-popup');
    popup.style.display = 'block'; // 팝업 표시
}

// 도서 반납 팝업 닫기
function closeReturnPopup() {
    document.querySelector('.popup.return-popup').style.display = 'none';
}

// 도서 반납 확인 버튼 클릭 시 호출되는 함수
function confirmReturn() {
    closeReturnPopup(); // 팝업 닫기

    fetch(`/return/${bookId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('반납 요청 실패');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                removeBookElement(bookId); // 도서 요소 삭제
                openReturnConfirmationPopup(); // 반납 완료 팝업 표시
            } else {
                alert('도서 반납에 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('도서 반납 중 오류가 발생했습니다.');
        });
}

// 특정 도서 요소 삭제
function removeBookElement(bookId) {
    const wrapper = document.getElementById(`wrapper-${bookId}`); // info-wrapper ID로 요소 선택
    if (wrapper) {
        wrapper.remove(); // wrapper 전체 삭제
    }
}

// 반납 성공 팝업 열기
function openReturnConfirmationPopup() {
    document.querySelector('.confirmation-popup').style.display = 'block';
    console.log('Confirmation popup displayed'); // 디버깅 로그 추가

    // 2초 후에 팝업 자동 닫기
    setTimeout(closeReturnConfirmationPopup, 2000);
}

// 반납 성공 팝업 닫기
function closeReturnConfirmationPopup() {
    document.querySelector('.confirmation-popup').style.display = 'none';
}
