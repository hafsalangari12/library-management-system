from flask import Flask, render_template, request, redirect, url_for, session
from app.models import db, Book


def create_app():
    app = Flask(__name__)
    app.secret_key = "secret123"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Login
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if username == "admin" and password == "admin":
                session["user"] = username
                return redirect(url_for("books"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect(url_for("login"))

    # Protect pages
    def is_logged_in():
        return "user" in session

    @app.route("/")
    def dashboard():
        if not is_logged_in():
            return redirect(url_for("login"))
        return render_template("dashboard.html")

    @app.route("/books")
    def books():
        if not is_logged_in():
            return redirect(url_for("login"))
        all_books = Book.query.all()
        return render_template("books.html", books=all_books)

    @app.route("/books/add", methods=["GET", "POST"])
    def add_book():
        if not is_logged_in():
            return redirect(url_for("login"))

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

    @app.route("/books/edit/<int:id>", methods=["GET", "POST"])
    def edit_book(id):
        if not is_logged_in():
            return redirect(url_for("login"))

        book = Book.query.get_or_404(id)

        if request.method == "POST":
            book.title = request.form["title"]
            book.author = request.form["author"]
            book.publication_year = request.form["publication_year"]
            book.language = request.form["language"]
            book.category = request.form["category"]

            db.session.commit()
            return redirect(url_for("books"))

        return render_template("edit_book.html", book=book)

    @app.route("/books/delete/<int:id>")
    def delete_book(id):
        if not is_logged_in():
            return redirect(url_for("login"))

        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("books"))

    @app.route("/books/toggle/<int:id>")
    def toggle_status(id):
        if not is_logged_in():
            return redirect(url_for("login"))

        book = Book.query.get_or_404(id)

        if book.status == "Available":
            book.status = "Checked Out"
        else:
            book.status = "Available"

        db.session.commit()
        return redirect(url_for("books"))

    return app