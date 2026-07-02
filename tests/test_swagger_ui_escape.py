from fastapi.openapi.docs import get_swagger_ui_init_js


def test_init_oauth_html_chars_are_escaped():
    xss_payload = "Evil</script><script>alert(1)</script>"
    js = get_swagger_ui_init_js(
        openapi_url="/openapi.json",
        init_oauth={"appName": xss_payload},
    )

    assert "</script><script>" not in js
    assert "\\u003c/script\\u003e\\u003cscript\\u003e" in js


def test_swagger_ui_parameters_html_chars_are_escaped():
    js = get_swagger_ui_init_js(
        openapi_url="/openapi.json",
        swagger_ui_parameters={"customKey": "<img src=x onerror=alert(1)>"},
    )
    assert "<img src=x onerror=alert(1)>" not in js
    assert "\\u003cimg" in js


def test_normal_init_oauth_still_works():
    js = get_swagger_ui_init_js(
        openapi_url="/openapi.json",
        init_oauth={"clientId": "my-client", "appName": "My App"},
    )
    assert '"clientId": "my-client"' in js
    assert '"appName": "My App"' in js
    assert "ui.initOAuth" in js
