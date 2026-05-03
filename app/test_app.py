from app import create_app

def test_home():
    app = create_app()
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 302  # redirects to login


def test_login_page():
    app = create_app()
    client = app.test_client()

    response = client.get("/login")
    assert response.status_code == 200