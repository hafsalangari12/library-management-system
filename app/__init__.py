from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def dashboard():
        return render_template("dashboard.html")

    return app