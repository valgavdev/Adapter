import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, HTTPBasic

from adapter import app_sets
from adapter.api.ts94 import TS94
from adapter.db import worker

security_basic = HTTPBasic(auto_error=False)
security_bearer = HTTPBearer()


def get_db():
    db = worker.Worker()
    try:
        yield db
    finally:
        db.close()


def check_token(auth: HTTPAuthorizationCredentials = Depends(security_bearer)):
    # token = auth.credentials
    # if not token:
    #     raise Exception('Не удалось проверить JWT')
    #
    # data = jwt.decode(token, app_sets.settings['JWT']['key'], algorithms='HS256')
    #
    # return data['user_id']
    pass


def get_ts94():
    return TS94(app_sets.get_ts94_sets())
