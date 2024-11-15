import pymysql
from app import app
from datetime import datetime

def get_mysql_connection():
    """
    MySQL 연결 객체 생성
    """
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE'],
        cursorclass=pymysql.cursors.DictCursor
    )

def insert_user(user_id, user_name):
    """
    사용자를 데이터베이스에 삽입
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO users (user_id, user_name) VALUES (%s, %s)"
            cursor.execute(query, (user_id, user_name))
            print("Insert query executed")  # 디버깅
        connection.commit()
        print("Data committed to database")  # 디버깅
        return True
    except Exception as e:
        print(f"Error inserting user: {e}")
        return False
    finally:
        connection.close()

def get_latest_user():
    """
    가장 최근에 삽입된 사용자 데이터 가져오기
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT user_id, user_name FROM users ORDER BY created_at DESC LIMIT 1"
            cursor.execute(query)
            return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        connection.close()

def get_user_by_id(user_id):
    """
    주어진 user_id로 사용자를 조회합니다.
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT user_id, user_name FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()  # 단일 결과 반환
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        connection.close()

def save_borrow_request(user_id, book_title, author, publisher, borrow_date, return_date):
    """
    대출 예약 정보를 데이터베이스에 저장.
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO borrow (user_id, book_title, author, publisher, borrow_date, return_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            rows_affected = cursor.execute(query, (user_id, book_title, author, publisher, borrow_date, return_date))
        connection.commit()
        return rows_affected > 0  # 영향받은 행이 있는지 확인
    except Exception as e:
        print(f"Error saving borrow request: {e}")
        return False
    finally:
        connection.close()


def get_borrowed_books():
    """
    대출된 책 정보를 가져옵니다.
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT book_title, author, publisher, borrow_date, return_date FROM borrow"
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching borrowed books: {e}")
        return []
    finally:
        connection.close()

from datetime import datetime, date  # `date`를 명시적으로 가져옵니다.

def get_borrowed_books_by_user(user_id):
    """
    주어진 user_id로 대출된 도서 정보를 조회하고, 연체 여부를 동적으로 확인.
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT id, book_title, author, publisher, borrow_date, return_date
            FROM borrow
            WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            books = cursor.fetchall()

            # 현재 날짜 가져오기
            current_date = date.today()

            # 연체 여부 동적 추가
            for book in books:
                # return_date가 date 타입인 경우 str로 변환
                if isinstance(book['return_date'], date):  # `date`를 사용합니다.
                    book['return_date'] = book['return_date'].strftime('%Y-%m-%d')

                # 연체 여부 계산
                return_date = datetime.strptime(book['return_date'], '%Y-%m-%d').date()
                book['status'] = '연체' if return_date < current_date else '대출중'

            return books
    except Exception as e:
        print(f"Error fetching borrowed books: {e}")
        return []
    finally:
        connection.close()


def delete_borrow_record(book_id):
    """
    데이터베이스에서 주어진 book_id를 삭제합니다.
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM borrow WHERE id = %s"
            print(f"Executing query: {query} with book_id: {book_id}")  # 디버깅 로그
            rows_affected = cursor.execute(query, (book_id,))
        connection.commit()
        print(f"Rows affected: {rows_affected}")  # 디버깅 로그
        return rows_affected > 0
    except Exception as e:
        print(f"Error deleting borrow record: {e}")
        return False
    finally:
        connection.close()



def check_user_exists(user_id):
    """
    데이터베이스에서 주어진 user_id가 존재하는지 확인합니다.
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result['COUNT(*)'] > 0  # 사용자 존재 여부 반환
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False
    finally:
        connection.close()

def get_borrowed_count_by_user(user_id):
    """
    주어진 user_id로 대출 중인 도서의 수를 조회합니다.
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) AS borrowed_count FROM borrow WHERE user_id = %s AND status = '대출중'"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result['borrowed_count']
    except Exception as e:
        print(f"Error fetching borrowed count: {e}")
        return 0
    finally:
        connection.close()

def return_book_in_database(book_id):
    """
    주어진 book_id의 도서를 반납 처리합니다.
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            # 반납 처리 (status를 반납완료로 업데이트)
            query = "UPDATE borrow SET status = '반납완료' WHERE id = %s"
            cursor.execute(query, (book_id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error returning book: {e}")
        return False
    finally:
        connection.close()