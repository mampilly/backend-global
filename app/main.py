
"""Main file"""
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from app.core import auth
from app.core.enum.api_name import APINAME
from app.routes.sample_module.controller import test_controller
from app.routes.users.controllers.user import user_controller
from app.routes.businesses.controller.business_metrics import business_metric_controller
from app.routes.businesses.controller.business_trends import business_trends_controller
from app.routes.businesses.controller.business import business_controller
from app.routes.businesses.controller.alerts import alerts_controller
from app.routes.socialmedia.controllers import social_media_controller
from app.core.config import config

app = FastAPI(docs_url=None, redoc_url=None)


def custom_openapi():
    """Custom Open API"""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=APINAME.api_name,
        version="3.0.2",
        description="This is an API that give access to API's",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://app.traice.io/assets/logos/logo.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://" + config.DB_USERNAME + \
    ":" + config.DB_PASSWORD + "@" + config.DB_HOST + ":" + config.DB_PORT + \
    "/" + config.DB_NAME


app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URL)

app.openapi = custom_openapi


@app.get("/endpoints", include_in_schema=False)
def overridden_swagger():
    """Swagger endpoint
    """
    return get_swagger_ui_html(openapi_url="/openapi.json", title=APINAME.api_name)


@app.get("/documentation", include_in_schema=False)
def overridden_redoc():
    """Api documentation end point"""
    return get_redoc_html(openapi_url="/openapi.json", title=APINAME.api_name)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(test_controller.router)
app.include_router(user_controller.router)
app.include_router(business_controller.router)
app.include_router(business_metric_controller.router)
app.include_router(business_trends_controller.router)
app.include_router(alerts_controller.router)
app.include_router(social_media_controller.router)


def use_route_names_as_operation_ids(application: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in application.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)
