import requests
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def fetch_books(keyword):
    """
    알라딘 API를 사용하여 키워드로 도서를 검색하는 함수.
    """
    api_url = "https://www.aladin.co.kr/ttb/api/ItemSearch.aspx"
    params = {
        'ttbkey': os.getenv('ALADIN_API_KEY'),  # 환경 변수에서 API 키 가져오기
        'Query': keyword,
        'QueryType': 'Title',
        'MaxResults': 3,
        'start': 1,
        'SearchTarget': 'Book',
        'output': 'js',
        'Version': '20131101'
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        
        # JSON 응답 파싱
        data = response.json()
        
        # 유효성 검사
        if 'item' not in data or not data['item']:
            print(f"검색 결과 없음: {keyword}")
            return None

        return data

    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류: {e}")
        return None
    except ValueError as e:  # JSON 파싱 실패 시
        print(f"응답 파싱 오류: {e}")
        return None

def fetch_new_books():
    """
    알라딘 API를 사용하여 신착도서를 가져오고 필요한 정보만 반환하는 함수.
    """
    api_url = "https://www.aladin.co.kr/ttb/api/ItemList.aspx"
    params = {
        'ttbkey': os.getenv('ALADIN_API_KEY'),  # 환경 변수에서 API 키 로드
        'QueryType': 'ItemNewAll',  # 신착도서 전체
        'MaxResults': 10,  # 최대 10권 가져오기
        'start': 1,
        'SearchTarget': 'Book',
        'output': 'js',
        'Version': '20131101'
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리

        data = response.json()
        items = data.get('item', [])

        # 필요한 정보만 추출하여 새로운 리스트 생성
        books = []
        for item in items:
            book = {
                'title': item['title'].split(' - ')[0],  # 제목에서 첫 부분만 추출
                'author': item['author'].split(' (')[0].strip(),  # 저자명만 추출
                'publisher': item['publisher'],
                'pubDate': item['pubDate'][:4],  # 출판년도만 추출
                'description': item['description'],
                'cover': item['cover'] if 'cover' in item and item['cover'] else '/static/img/default-cover.png'
            }
            books.append(book)

        return books  # 필터링된 도서 리스트 반환

    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류: {e}")
        return []
    except ValueError as e:
        print(f"응답 파싱 오류: {e}")
        return []
