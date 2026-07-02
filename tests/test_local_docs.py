import inspect
from urllib.parse import urljoin

from fastapi.openapi.docs import (
    get_redoc_css,
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
    get_swagger_ui_oauth2_redirect_js,
)


def test_strings_in_generated_swagger():
    sig = inspect.signature(get_swagger_ui_html)
    swagger_js_url = sig.parameters.get("swagger_js_url").default  # type: ignore
    swagger_css_url = sig.parameters.get("swagger_css_url").default  # type: ignore
    swagger_favicon_url = sig.parameters.get("swagger_favicon_url").default  # type: ignore
    swagger_ui_init_script_url = sig.parameters.get(  # type: ignore
        "swagger_ui_init_script_url"
    ).default
    html = get_swagger_ui_html(title="title")
    body_content = bytes(html.body).decode()
    assert swagger_js_url in body_content
    assert swagger_css_url in body_content
    assert swagger_favicon_url in body_content
    assert f'<script src="{swagger_ui_init_script_url}">' in body_content


def test_strings_in_custom_swagger():
    swagger_js_url = "swagger_fake_file.js"
    swagger_css_url = "swagger_fake_file.css"
    swagger_favicon_url = "swagger_fake_file.png"
    swagger_ui_init_script_url = "custom-swagger-initializer.js"
    html = get_swagger_ui_html(
        title="title",
        swagger_js_url=swagger_js_url,
        swagger_css_url=swagger_css_url,
        swagger_favicon_url=swagger_favicon_url,
        swagger_ui_init_script_url=swagger_ui_init_script_url,
    )
    body_content = bytes(html.body).decode()
    assert swagger_js_url in body_content
    assert swagger_css_url in body_content
    assert swagger_favicon_url in body_content
    assert f'<script src="{swagger_ui_init_script_url}">' in body_content


def test_default_swagger_ui_init_script_url_resolves_under_default_docs_url():
    sig = inspect.signature(get_swagger_ui_html)
    swagger_ui_init_script_url = sig.parameters.get(  # type: ignore
        "swagger_ui_init_script_url"
    ).default
    docs_url = "http://testserver/docs"
    assert urljoin(docs_url, swagger_ui_init_script_url) == (
        "http://testserver/docs/swagger-initializer.js"
    )


def test_strings_in_generated_redoc():
    sig = inspect.signature(get_redoc_html)
    redoc_js_url = sig.parameters.get("redoc_js_url").default  # type: ignore
    redoc_favicon_url = sig.parameters.get("redoc_favicon_url").default  # type: ignore
    redoc_css_url = sig.parameters.get("redoc_css_url").default  # type: ignore
    html = get_redoc_html(openapi_url="/docs", title="title")
    body_content = bytes(html.body).decode()
    assert redoc_js_url in body_content
    assert redoc_favicon_url in body_content
    assert f'<link rel="stylesheet" type="text/css" href="{redoc_css_url}">' in (
        body_content
    )


def test_strings_in_custom_redoc():
    redoc_js_url = "fake_redoc_file.js"
    redoc_favicon_url = "fake_redoc_file.png"
    redoc_css_url = "fake_redoc.css"
    html = get_redoc_html(
        openapi_url="/docs",
        title="title",
        redoc_js_url=redoc_js_url,
        redoc_favicon_url=redoc_favicon_url,
        redoc_css_url=redoc_css_url,
    )
    body_content = bytes(html.body).decode()
    assert redoc_js_url in body_content
    assert redoc_favicon_url in body_content
    assert f'<link rel="stylesheet" type="text/css" href="{redoc_css_url}">' in (
        body_content
    )


def test_default_redoc_css_url_resolves_under_default_redoc_url():
    sig = inspect.signature(get_redoc_html)
    redoc_css_url = sig.parameters.get("redoc_css_url").default  # type: ignore
    redoc_url = "http://testserver/redoc"
    assert urljoin(redoc_url, redoc_css_url) == "http://testserver/redoc/redoc.css"


def test_google_fonts_in_generated_redoc():
    body_with_google_fonts = bytes(
        get_redoc_html(openapi_url="/docs", title="title").body
    ).decode()
    assert "fonts.googleapis.com" in body_with_google_fonts
    body_without_google_fonts = bytes(
        get_redoc_html(openapi_url="/docs", title="title", with_google_fonts=False).body
    ).decode()
    assert "fonts.googleapis.com" not in body_without_google_fonts


def test_custom_google_fonts_css_url_in_generated_redoc():
    google_fonts_css_url = "https://example.com/fonts.css"
    html = get_redoc_html(
        openapi_url="/docs", title="title", google_fonts_css_url=google_fonts_css_url
    )
    body_content = bytes(html.body).decode()
    assert f'<link href="{google_fonts_css_url}" rel="stylesheet">' in body_content
    assert "fonts.googleapis.com" not in body_content


def test_get_redoc_css():
    css = get_redoc_css()
    assert "margin:0" in css
    assert "padding:0" in css


def test_strings_in_generated_swagger_oauth2_redirect():
    sig = inspect.signature(get_swagger_ui_oauth2_redirect_html)
    oauth2_redirect_script_url = sig.parameters.get(  # type: ignore
        "oauth2_redirect_script_url"
    ).default
    html = get_swagger_ui_oauth2_redirect_html()
    body_content = bytes(html.body).decode()
    assert f'<script src="{oauth2_redirect_script_url}">' in body_content


def test_strings_in_custom_swagger_oauth2_redirect():
    oauth2_redirect_script_url = "fake-oauth2-redirect.js"
    html = get_swagger_ui_oauth2_redirect_html(
        oauth2_redirect_script_url=oauth2_redirect_script_url
    )
    body_content = bytes(html.body).decode()
    assert f'<script src="{oauth2_redirect_script_url}">' in body_content


def test_get_swagger_ui_oauth2_redirect_js():
    js = get_swagger_ui_oauth2_redirect_js()
    assert "swaggerUIRedirectOauth2" in js
