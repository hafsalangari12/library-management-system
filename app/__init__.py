from flask import Flask, render_template, request, redirect, url_for, session
from app.models import db, Book, User, History


def create_app():
    app = Flask(__name__)
    app.secret_key = "secret123"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

        # Create sample users if empty
        if User.query.count() == 0:
            db.session.add_all([
                User(name="Hafsa Langari"),
                User(name="Hafizullah Khplwak"),
                User(name="Mufeedullah Mamozai"),
                User(name="Sapida Muska Masood")
            ])
            db.session.commit()

    # ---------------- LOGIN ----------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None

        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if username == "admin" and password == "admin":
                session["user"] = username
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid username or password"

        return render_template("login.html", error=error)

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect(url_for("login"))

    def is_logged_in():
        return "user" in session

    # ---------------- DASHBOARD ----------------
    @app.route("/")
    def dashboard():
        if not is_logged_in():
            return redirect(url_for("login"))
        return render_template("dashboard.html")

    # ---------------- BOOKS (WITH SEARCH) ----------------
    @app.route("/books")
    def books():
        if not is_logged_in():
            return redirect(url_for("login"))

        query = request.args.get("q")

        if query:
            all_books = Book.query.filter(
                Book.title.contains(query) | Book.author.contains(query)
            ).all()
        else:
            all_books = Book.query.all()

        return render_template("books.html", books=all_books)

    # ---------------- ADD BOOK ----------------
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

    # ---------------- EDIT BOOK ----------------
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

    # ---------------- DELETE BOOK ----------------
    @app.route("/books/delete/<int:id>")
    def delete_book(id):
        if not is_logged_in():
            return redirect(url_for("login"))

        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("books"))

    # ---------------- CHECKOUT / RETURN WITH HISTORY ----------------
    @app.route("/books/toggle/<int:id>")
    def toggle_status(id):
        if not is_logged_in():
            return redirect(url_for("login"))

        book = Book.query.get_or_404(id)

        if book.status == "Available":
            user = User.query.first()
            book.status = "Checked Out"

            history = History(
                book_id=book.id,
                user_id=user.id,
                action="Checked Out"
            )
            db.session.add(history)

        else:
            book.status = "Available"

            history = History(
                book_id=book.id,
                user_id=None,
                action="Returned"
            )
            db.session.add(history)

        db.session.commit()
        return redirect(url_for("books"))

    # ---------------- HISTORY PAGE ----------------
    @app.route("/history")
    def history():
        if not is_logged_in():
            return redirect(url_for("login"))

        records = History.query.order_by(History.timestamp.desc()).all()
        return render_template("history.html", records=records)

    return app