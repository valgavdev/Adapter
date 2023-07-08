import contextvars
import types


request_global = contextvars.ContextVar("request_global",
                                        default=types.SimpleNamespace(ip=None, id=None, user_id=None))


def g():
    if request_global:
        return request_global.get()

    return None