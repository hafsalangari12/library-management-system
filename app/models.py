from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ---------------- USER (MEMBER) ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"


# ---------------- BOOK ----------------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(80), nullable=True)
    status = db.Column(db.String(20), default="Available")

    def __repr__(self):
        return f"<Book {self.title}>"


# ---------------- HISTORY ----------------
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    action = db.Column(db.String(50))  # Checked Out / Returned
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    book = db.relationship('Book')
    user = db.relationship('User')