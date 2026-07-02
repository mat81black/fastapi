from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(
    docs_url="/docs/",
    redoc_url="/redoc/",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect/",
)


client = TestClient(app)


def test_swagger_ui_init_script_url_has_no_double_slash():
    response = client.get("/docs/")
    assert response.status_code == 200, response.text
    assert '<script src="/docs/swagger-initializer.js">' in response.text
    assert "swagger-initializer.js//" not in response.text


def test_swagger_ui_init_script_is_served():
    response = client.get("/docs/swagger-initializer.js")
    assert response.status_code == 200, response.text


def test_oauth2_redirect_script_url_has_no_double_slash():
    response = client.get("/docs/oauth2-redirect/")
    assert response.status_code == 200, response.text
    assert '<script src="/docs/oauth2-redirect.js">' in response.text


def test_oauth2_redirect_script_is_served():
    response = client.get("/docs/oauth2-redirect.js")
    assert response.status_code == 200, response.text


def test_redoc_css_url_has_no_double_slash():
    response = client.get("/redoc/")
    assert response.status_code == 200, response.text
    assert '<link rel="stylesheet" type="text/css" href="/redoc/redoc.css">' in (
        response.text
    )


def test_redoc_css_is_served():
    response = client.get("/redoc/redoc.css")
    assert response.status_code == 200, response.text
