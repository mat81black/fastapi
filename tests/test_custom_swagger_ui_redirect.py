from fastapi import FastAPI
from fastapi.testclient import TestClient

swagger_ui_oauth2_redirect_url = "/docs/redirect"

app = FastAPI(swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


def test_swagger_ui():
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "swagger-ui-dist" in response.text
    print(client.base_url)
    assert '<script src="/docs/swagger-initializer.js">' in response.text


def test_swagger_ui_init_script():
    response = client.get("/docs/swagger-initializer.js")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/javascript; charset=utf-8"
    assert (
        f"oauth2RedirectUrl: window.location.origin + '{swagger_ui_oauth2_redirect_url}'"
        in response.text
    )


def test_swagger_ui_oauth2_redirect():
    response = client.get(swagger_ui_oauth2_redirect_url)
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert f'<script src="{swagger_ui_oauth2_redirect_url}.js">' in response.text


def test_swagger_ui_oauth2_redirect_script():
    response = client.get(f"{swagger_ui_oauth2_redirect_url}.js")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/javascript; charset=utf-8"
    assert "window.opener.swaggerUIRedirectOauth2" in response.text


def test_response():
    response = client.get("/items/")
    assert response.json() == {"id": "foo"}
