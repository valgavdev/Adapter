from fastapi import FastAPI

from . import openapi
from . import middlewares

app = FastAPI(
                           # hide schemas
                           swagger_ui_parameters={"defaultModelsExpandDepth": -1, "syntaxHighlight": False})

app.middleware('http')(middlewares.middleware_exception_handler)
app.middleware('http')(middlewares.LoggingMiddleware())

from .v1 import router_v1


app.include_router(router_v1)

openapi.custom_openapi(app)

@app.get("/")
def test_connect():

    return "ADAPTER"

