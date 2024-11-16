let selectedBookData = null;

// 팝업 열기
function openPopup(bookData) {
    selectedBookData = bookData;
    document.querySelector('.popup').style.display = 'block';
}

// 팝업 닫기
function closePopup() {
    selectedBookData = null;
    document.querySelector('.popup').style.display = 'none';
}

// 도서 예약 함수
function reserveBook(buttonElement) {
    const bookElement = buttonElement.closest('.book');
    const bookData = {
        title: bookElement.dataset.title,
        author: bookElement.dataset.author,
        publisher: bookElement.dataset.publisher,
    };

    openPopup(bookData);
}

// 예약 확인 후 서버 전송
function confirmReservation() {
    if (!selectedBookData) return;

    console.log('Sending data:', selectedBookData); // 전송 데이터 확인

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: selectedBookData.title,
            author: selectedBookData.author,
            publisher: selectedBookData.publisher,
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data); // 서버 응답 확인
            if (data.success) {
                openConfirmationPopup(); // 예약 성공 팝업 표시
            } else {
                alert(data.message || '예약에 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('Error reserving book:', error); // 오류 로그
            alert('서버 오류가 발생했습니다.');
        })
        .finally(() => closePopup());
}
    
// 예약 성공 팝업
function openConfirmationPopup() {
    const popup = document.querySelector('.confirmation-popup');
    popup.style.display = 'block';

    setTimeout(() => {
        popup.style.display = 'none';
    }, 2000);
}
