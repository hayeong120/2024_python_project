import pymysql
from app import app

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
