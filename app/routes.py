from flask import render_template, request, redirect, url_for
from app import app
from app.models import insert_user, get_latest_user
from app.utils import fetch_books

# 초기 시작 페이지
@app.route('/')
def start():
    return render_template('start.html')

# 로그인 페이지
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        # 폼 데이터 받기
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        print(f"Received user_id: {user_id}, user_name: {user_name}")  # 디버깅

        # MySQL에 데이터 삽입
        if insert_user(user_id, user_name):
            print("User inserted successfully")  # 디버깅
            return redirect(url_for('main'))
        else:
            print("Failed to insert user")  # 디버깅
            return "Error: 사용자를 저장할 수 없습니다.", 500
    return render_template('user.html')

# 메인 페이지 (허브 역할)
@app.route('/main')
def main():
    user_data = get_latest_user()
    user_id = user_data['user_id'] if user_data else None
    user_name = user_data['user_name'] if user_data else None

    return render_template('main.html', user_id=user_id, user_name=user_name)

# 도서 대출 및 반납 페이지
@app.route('/management')
def management():
    return render_template('management.html')

# 반납 페이지
@app.route('/return')
def return_page():
    return render_template('return.html')

# 대출 페이지
@app.route('/borrow')
def borrow():
    return render_template('borrow.html')

# 사용자 페이지
@app.route('/myBook')
def my_book():
    return render_template('myBook.html')

# 책 검색 페이지 (인기도서와 신착도서 포함)
@app.route('/search')
def search():
    return render_template('search.html')

# 특정 도서 상세 정보 페이지
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
