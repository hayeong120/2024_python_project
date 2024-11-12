from flask import render_template, request
from app import app
from app.utils import fetch_books

@app.route('/')
def index():
    return render_template('bookInfo.html', book=None)

@app.route('/bookInfo')
def book_info():
    keyword = request.args.get('keyword')
    book_data = fetch_books(keyword) if keyword else None
    if book_data and 'item' in book_data:
        # 필요한 데이터만 추출하여 변수에 할당
        title = book_data['item'][0]['title'].split(' - ')[0]  # 제목에서 첫 부분만 가져오기
        author = book_data['item'][0]['author'].split(' (')[0].strip()  # 저자명만 가져오기
        publisher = book_data['item'][0]['publisher']
        pub_date = book_data['item'][0]['pubDate'][:4]  # 출판년도만 가져오기
        description = book_data['item'][0]['description']
        cover = book_data['item'][0]['cover']
        
        # book 객체에 수정된 데이터 할당
        book = {
            'title': title,
            'author': author,
            'publisher': publisher,
            'pubDate': pub_date,
            'description': description,
            'cover': cover
        }
    else:
        book = None

    return render_template('bookInfo.html', book=book)
