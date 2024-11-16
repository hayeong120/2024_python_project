import requests

# 알라딘 API 요청을 위한 유틸리티 함수
def fetch_books(keyword):
    api_url = "https://www.aladin.co.kr/ttb/api/ItemSearch.aspx"
    params = {
        'ttbkey': 'ttbjbg012002491946002',
        'Query': keyword,
        'QueryType': 'Title',
        'MaxResults': 10,
        'start': 1,
        'SearchTarget': 'Book',
        'output': 'js',
        'Version': '20131101'  
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return None


def fetch_new_books():
    """
    알라딘 API를 통해 신착 도서 정보를 가져오는 함수
    """
    api_url = "https://www.aladin.co.kr/ttb/api/ItemList.aspx"
    params = {
        'ttbkey': 'ttbjbg012002491946002',
        'QueryType': 'ItemNewAll',  # 신착 도서 목록 조회
        'MaxResults': 3,  # 최대 결과 수
        'start': 1,
        'SearchTarget': 'Book',
        'output': 'js',
        'Version': '20131101'
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 요청 실패 시 예외 발생
        data = response.json()

        # 필요한 데이터만 추출하여 리스트로 반환
        books = [
            {
                'book_title': item.get('title', '제목 없음').split(' - ')[0],  # 제목에서 첫 부분만 가져오기
                'author': item.get('author', '저자 미상').split(' (')[0].strip(),  # 저자명만 가져오기
                'publisher': item.get('publisher', '출판사 미상'),
                'cover_image': item.get('cover', '기본 이미지 경로')
            }
            for item in data.get('item', [])
        ]
        return books

    except requests.RequestException as e:
        print(f"신착 도서 요청 중 오류 발생: {e}")
        return []
