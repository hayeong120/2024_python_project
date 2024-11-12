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
    openConfirmationPopup(); // 두 번째 팝업 열기
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
