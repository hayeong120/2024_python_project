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
        response.raise_for_status()  # 요청에 실패하면 예외 발생
        return response.json()       # JSON 응답을 반환
    except requests.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return None
