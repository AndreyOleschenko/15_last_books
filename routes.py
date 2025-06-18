import os

from flask import Flask, render_template, request, jsonify, redirect, url_for
from app import app, db
from app.models import Book, Genre


with app.app_context():
    db.create_all()  

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def index():
    books = Book.query.order_by(Book.id.desc()).limit(15).all()
    genres = Genre.query.all()
    return render_template('index.html', books=books, genres=genres)

@app.route('/genre/<int:genre_id>')
def genre_page(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    books = Book.query.filter_by(genre_id=genre_id).order_by(Book.id.desc()).all()
    return render_template('genre.html', genre=genre, books=books)

@app.route('/update_is_read/<int:book_id>', methods=['POST'])
def update_is_read(book_id):
    book = Book.query.get_or_404(book_id)
    is_read = request.json.get('is_read', False)
    book.is_read = is_read
    db.session.commit()
    return jsonify({'success': True, 'is_read': book.is_read})

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    genre_id = request.form.get('genre_id')
    if title and author and genre_id:
        book = Book(title=title, author=author, genre_id=genre_id)
        db.session.add(book)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_genre', methods=['POST'])
def add_genre():
    name = request.form.get('genre_name')
    if name:
        genre = Genre(name=name)
        db.session.add(genre)
        db.session.commit()
    return redirect(url_for('index'))

