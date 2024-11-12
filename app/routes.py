from flask import render_template, request
from app import app
from app.utils import fetch_books

@app.route('/')
def index():
    return render_template('index.html', book=None)

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    book_data = fetch_books(keyword) if keyword else None
    book = book_data['item'][0] if book_data and 'item' in book_data else None
    return render_template('index.html', book=book) 
