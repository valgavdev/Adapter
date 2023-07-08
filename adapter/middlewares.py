import types
import uuid

from contextlib import asynccontextmanager
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse, Response
from starlette.types import Message

from .v1 import router_v1
from . import exceptions, requestvars

from .logger import http_logger


class LoggingMiddleware:
    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        async def receive() -> Message:
            return {'type': 'http.request', 'body': body}

        request._receive = receive

    async def get_body(self, request: Request) -> bytes:
        body = await request.body()
        await self.set_body(request, body)
        return body

    async def __call__(self, request: Request, call_next, *args, **kwargs):
        request_body = await request.body()
        await self.set_body(request, request_body)
        request_body = await self.get_body(request)

        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.client.host
        initial_g = types.SimpleNamespace(ip=ip, id=str(uuid.uuid4()), user_id=None)
        requestvars.request_global.set(initial_g)

        http_logger.info(f'url: {request.url}\n\theaders: {request.headers}\n\tbody: {request_body}')

        response = await call_next(request)
        response_body = b''
        async for chunk in response.body_iterator:
            response_body += chunk

        response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
        if len(response_body) > 1000:
            response_body = response_body[:1000]

        http_logger.info(f'{request_body.decode()}\n\t-> {response_body.decode()}')

        return response


"""
async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


@app.middleware("http")
async def init_global(request: Request, call_next):
    await set_body(request, await request.body())
    body = await get_body(request)

    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.client.host
    id = str(uuid.uuid4())
    user_id = None

    initial_g = types.SimpleNamespace(ip=ip, id=id, user_id=user_id, rpc_id=None)
    requestvars.request_global.set(initial_g)

    logger.info(f'body: {body}')

    response = await call_next(request)

    return response
"""


# @asynccontextmanager
# async def middleware_logging(ctx: jsonrpc.JsonRpcContext):
#     requestvars.g().rpc_id = ctx.raw_request.get('id')
#
#     http_logger.info(f'{ctx.raw_request}')
#     try:
#         yield
#     finally:
#         if len(str(ctx.raw_response)) > 1000:
#             http_logger.info(f'{ctx.raw_request} -> ...')
#         else:
#             http_logger.info(f'{ctx.raw_request} -> {ctx.raw_response}')

async def middleware_exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except exceptions.BaseException as ex:
        http_logger.exception(f'{ex!r}')
        return JSONResponse(status_code=200, content={"code": ex.code, "message": ex.message})
    except Exception as ex:
        http_logger.exception(f'{ex!r}')
        return JSONResponse(status_code=200, content={"code": -1, "message": str(ex)})

# @asynccontextmanager
# async def middleware_exception_handler(ctx: jsonrpc.JsonRpcContext):
#     try:
#         yield
#     except SQLServerDBException as e:
#         http_logger.exception(f'{e!r}')
#
#         raise JSONRPCError(e.message, e.code)
#     except exceptionex.ExceptionEx as e:
#         http_logger.exception(f'{e!r}')
#
#         if config.debug:
#             data = {'func_name': e.func_name, 'data': e.data}
#         else:
#             data = e.data
#
#         raise JSONRPCError(e.message, e.code, data=data)
#     except jsonrpc.BaseError as e:
#         http_logger.exception(f'{e!r}')
#
#         raise
#     except Exception as e:
#         http_logger.exception(f'{e!r}')
#
#         raise UnknownError(data=f'{e!r}')
