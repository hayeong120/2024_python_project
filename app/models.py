import pymysql
from app import app
from datetime import datetime, date

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
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting user: {e}")
        return False
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
            return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        connection.close()

def save_borrow_request(user_id, book_title, author, publisher, borrow_date, return_date, cover_image):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            # 대출 요청 삽입
            query = """
            INSERT INTO borrow (user_id, book_title, author, publisher, borrow_date, return_date, cover_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, book_title, author, publisher, borrow_date, return_date, cover_image))
            
            # borrow_count 증가
            update_query = """
            UPDATE borrow
            SET borrow_count = borrow_count + 1
            WHERE book_title = %s
            """
            cursor.execute(update_query, (book_title,))
            
        connection.commit()
        return True
    except Exception as e:
        print(f"Error saving borrow request or updating borrow_count: {e}")
        return False
    finally:
        connection.close()

def get_borrowed_books_by_user(user_id):
    """
    주어진 user_id로 대출 중인 도서 정보를 반환합니다.
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT book_title, author, publisher, borrow_date, return_date
            FROM borrow
            WHERE user_id = %s AND return_date > CURRENT_DATE
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()  # 대출 중인 책 목록 반환
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
            cursor.execute(query, (book_id,))
        connection.commit()
        return True
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
            query = "SELECT COUNT(*) AS count FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result['count'] > 0
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False
    finally:
        connection.close()

def update_borrow_count(book_title):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            UPDATE borrow
            SET borrow_count = borrow_count + 1
            WHERE book_title = %s
            """
            cursor.execute(query, (book_title,))
        connection.commit()
    except Exception as e:
        print(f"Error updating borrow_count: {e}")
    finally:
        connection.close()

def save_reserve_request(user_id, book_title, author, publisher, cover_image):
    """
    reservations 테이블에 대출 예약 정보를 저장
    """
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO reservations (user_id, book_title, author, publisher, reserved_at, cover_image)
            VALUES (%s, %s, %s, %s, NOW(), %s)
            """
            cursor.execute(query, (user_id, book_title, author, publisher, cover_image))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error saving reservation: {e}")
        return False
    finally:
        connection.close()

