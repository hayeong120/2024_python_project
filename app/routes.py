from flask import render_template, request, redirect, url_for, jsonify, session
from app import app
from app.models import (
    insert_user, get_user_by_id, save_borrow_request, check_user_exists,
    get_borrowed_books_by_user, delete_borrow_record, update_borrow_count, save_reserve_request
)
from app.utils import fetch_books, fetch_new_books
from datetime import datetime, timedelta

# 공통 유틸리티 함수: 로그인 여부 확인
def is_logged_in():
    user_id = session.get('user_id')
    if not user_id:
        return False
    return user_id


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

        # 세션에 사용자 ID 저장
        session['user_id'] = user_id

        # 사용자 중복 확인 및 삽입
        if not check_user_exists(user_id):
            if not insert_user(user_id, user_name):
                return "Error: 사용자를 저장할 수 없습니다.", 500

        return redirect(url_for('main'))
    return render_template('user.html')

# 메인 페이지
@app.route('/main')
def main():
    user_id = is_logged_in()
    if not user_id:
        return redirect(url_for('user'))

    user_data = get_user_by_id(user_id)
    user_name = user_data['user_name'] if user_data else "사용자"

    return render_template('main.html', user_id=user_id, user_name=user_name)

# 도서 대출 및 반납 페이지
@app.route('/management')
def management():
    return render_template('management.html')

# 반납 페이지
@app.route('/return', methods=['GET'])
def return_page():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('user'))

    # 사용자의 대출 도서 데이터 가져오기
    books = get_borrowed_books_by_user(user_id)
    print(f"Borrowed books: {books}")  # 디버깅용 출력

    return render_template('return.html', books=books)

@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    try:
        if delete_borrow_record(book_id):  # 수정: 삭제된 함수 대신 새 함수 호출
            return jsonify({'success': True, 'message': '도서 반납 성공'})
        else:
            return jsonify({'success': False, 'message': '도서를 찾을 수 없습니다.'}), 404
    except Exception as e:
        print(f"Error in return_book: {e}")  # 디버깅 로그
        return jsonify({'success': False, 'message': f'서버 오류: {e}'}), 500

# 대출 페이지
@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    user_id = is_logged_in()
    if not user_id:
        return redirect(url_for('user'))

    user = get_user_by_id(user_id)

    book = None
    # 도서 검색
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        if keyword:
            book_data = fetch_books(keyword)
            if book_data and 'item' in book_data:
                first_book = book_data['item'][0]
                book = {
                    'title': first_book['title'].split(' - ')[0],
                    'author': first_book['author'].split(' (')[0].strip(),
                    'publisher': first_book['publisher'],
                    'pubDate': first_book['pubDate'][:4],
                    'description': first_book['description'],
                    'cover': first_book['cover']
                }

    # 대출 도서 저장
    elif request.method == 'POST':
        book_title = request.form.get('book_title')
        author = request.form.get('author')
        publisher = request.form.get('publisher')
        cover_image = request.form.get('cover_image')

        # 대출 중인 책 수 확인
        borrowed_books = get_borrowed_books_by_user(user_id)
        borrowed_count = len(borrowed_books)  # 현재 대출 중인 책의 개수

        if borrowed_count >= 4:  # 대출 제한 확인
            return jsonify({'success': False, 'message': '대출 한도 초과'}), 200

        # 대출 처리
        borrow_date = datetime.now().strftime('%Y-%m-%d')
        return_date = (datetime.now() + timedelta(weeks=2)).strftime('%Y-%m-%d')

        # 대출 요청 저장
        if save_borrow_request(user_id, book_title, author, publisher, borrow_date, return_date, cover_image):
            return jsonify({'success': True, 'return_date': return_date})
        else:
            return jsonify({'success': False, 'message': '대출 예약 실패'}), 500

    return render_template('borrow.html', book=book)

# 사용자 페이지
@app.route('/myBook')
def myBook():
    return render_template('myBook.html')

# 책 검색 페이지
@app.route('/search', methods=['GET'])
def search_page():
    try:
        new_books = fetch_new_books()[:3]  # 최대 3개만 가져오기
        print(f"신착도서 데이터: {new_books}")  # 신착도서 데이터 출력
    except Exception as e:
        print(f"Error fetching new books: {e}")
        new_books = []

    popular_books = [
        {"book_title": "채식주의자", "author": "한강", "publisher": "창비", "cover_image": "/static/img/sample-book.png"},
        {"book_title": "뜨거운 홍차", "author": "김빵", "publisher": "문페이스", "cover_image": "/static/img/sample-book2.png"},
        {"book_title": "용서받지 못한 밤", "author": "미치오 슈스케", "publisher": "놀", "cover_image": "/static/img/sample-book3.png"},
    ]

    return render_template('search.html', new_books=new_books, popular_books=popular_books)

@app.route('/reserve', methods=['POST'])
def reserve_book():
    data = request.get_json()
    print(f"Received data for reservation: {data}")  # 디버깅용 출력

    if not data:
        return jsonify({'success': False, 'message': '필수 데이터 누락'}), 400

    # 데이터 추출
    title = data.get('title')
    author = data.get('author')
    publisher = data.get('publisher')
    cover_image = data.get('cover_image')

    # 필수 데이터 확인
    if not title or not author or not publisher or not cover_image:
        print("필수 데이터 누락")
        return jsonify({'success': False, 'message': '필수 데이터 누락'}), 400

    # 세션에서 user_id 가져오기
    user_id = session.get('user_id')
    if not user_id:
        print("User ID 누락")
        return jsonify({'success': False, 'message': '사용자 정보를 확인하세요.'}), 400

    # 데이터베이스 저장 시도
    try:
        if save_reserve_request(user_id, title, author, publisher, cover_image):
            return jsonify({'success': True})
        else:
            print("데이터베이스 저장 실패")
            return jsonify({'success': False, 'message': '서버 오류 발생'}), 500
    except Exception as e:
        print(f"Error saving reservation: {e}")
        return jsonify({'success': False, 'message': '서버 오류 발생'}), 500
