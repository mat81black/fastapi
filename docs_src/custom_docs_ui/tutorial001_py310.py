from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_init_js,
    get_swagger_ui_oauth2_redirect_html,
    get_swagger_ui_oauth2_redirect_js,
)
from fastapi.responses import Response

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs/swagger-initializer.js", include_in_schema=False)
async def swagger_ui_init_script():
    js = get_swagger_ui_init_js(
        openapi_url=app.openapi_url,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    )
    return Response(content=js, media_type="text/javascript")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        title=app.title + " - Swagger UI",
        swagger_ui_init_script_url="/docs/swagger-initializer.js",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/docs/oauth2-redirect.js", include_in_schema=False)
async def oauth2_redirect_script():
    js = get_swagger_ui_oauth2_redirect_js()
    return Response(content=js, media_type="text/javascript")


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html(
        oauth2_redirect_script_url="/docs/oauth2-redirect.js",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )


@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
