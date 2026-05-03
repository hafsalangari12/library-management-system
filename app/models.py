from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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