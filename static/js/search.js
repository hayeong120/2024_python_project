document.addEventListener('DOMContentLoaded', () => {
    // 클릭 이벤트 리스너
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('reserve-btn')) {
            // 버튼이 포함된 책 요소를 찾기
            const bookElement = e.target.closest('.book');
            if (!bookElement) {
                console.error('Book element not found');
                return;
            }

            // 책 데이터 추출
            const bookData = {
                title: bookElement.dataset.title,
                author: bookElement.dataset.author,
                publisher: bookElement.dataset.publisher,
                cover_image: bookElement.dataset.cover,
            };

            console.log('Book data:', bookData); // 디버깅용 출력

            // 데이터 유효성 검사
            if (!bookData.title || !bookData.author || !bookData.publisher || !bookData.cover_image) {
                alert('필수 데이터가 누락되었습니다.');
                return;
            }

            // 팝업 열기
            openPopup(bookData);
        }
    });

    // "확인" 버튼 클릭 이벤트
    document.getElementById('confirm-btn').addEventListener('click', function () {
        if (!selectedBookData) {
            console.error('No selected book data');
            return;
        }

        console.log('Sending data to server:', selectedBookData);

        fetch('/reserve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(selectedBookData),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Server response:', data); // 서버 응답 디버깅
                if (data.success) {
                    openConfirmationPopup();
                } else {
                    alert(data.message || '예약에 실패했습니다.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('서버 오류가 발생했습니다.');
            })
            .finally(() => closePopup());
    });
});

let selectedBookData = null;

// 팝업 열기
function openPopup(bookData) {
    selectedBookData = bookData;

    const popupElement = document.querySelector('.popup');
    if (!popupElement) {
        console.error('Popup element not found');
        return;
    }

    popupElement.style.display = 'block';
}

// 팝업 닫기
function closePopup() {
    selectedBookData = null;

    const popupElement = document.querySelector('.popup');
    if (!popupElement) {
        console.error('Popup element not found');
        return;
    }

    popupElement.style.display = 'none';
}

// 예약 성공 팝업 열기
function openConfirmationPopup() {
    const popup = document.querySelector('.confirmation-popup');
    if (!popup) {
        console.error('Confirmation popup not found');
        return;
    }

    popup.style.display = 'block';
    setTimeout(() => {
        popup.style.display = 'none';
    }, 2000);
}
