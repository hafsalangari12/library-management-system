from flask import Flask, render_template, request, redirect, url_for
from app.models import db, Book


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/books")
    def books():
        all_books = Book.query.all()
        return render_template("books.html", books=all_books)

    @app.route("/books/add", methods=["GET", "POST"])
    def add_book():
        if request.method == "POST":
            new_book = Book(
                title=request.form["title"],
                author=request.form["author"],
                publication_year=request.form["publication_year"],
                language=request.form["language"],
                category=request.form["category"],
            )
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for("books"))

        return render_template("add_book.html")

    return app