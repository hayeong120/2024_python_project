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
