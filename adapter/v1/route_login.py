import jwt
import datetime

from typing import Optional
from fastapi import Depends, Body
from fastapi.security import HTTPBasicCredentials

from adapter import app_sets
from . import router_v1
from .. import dependencies


@router_v1.method('/login', tags=['Autorization'], summary='Авторизация', response_description='JWT')
def login(username: Optional[str] = Body(None, example='username'),
          password: Optional[str] = Body(None, example='password'),
          auth: Optional[HTTPBasicCredentials] = Depends(dependencies.security_basic),
          db=Depends(dependencies.get_db)) -> str:
    """
    Логин и пароль могут передаваться как в заголовке, так и в параметрах метода.

    В заголовке (можно воспользоваться кнопкой Authorize):

        Authorization:Basic <данные пользователя>

        <данные пользователя> - строка, содержащая логин и пароль, разделенные двоеточием, и закодированная в base64.

    После авторизации клиент получает JWT, который используется для формирования запросов.

    JWT помещается в заголовок в поле «Authorization» (можно воспользоваться кнопкой Authorize):

        Authorization:Bearer <JWT>
    """

    if auth and auth.username and auth.password:
        username = auth.username
        password = auth.password

    if not username or not password:
        raise Exception('Invalid auth')#exceptions.ErrorAutorization()

    user = db.user_check_auth(username, password)

    return jwt.encode({'user_id': user.guid,
                       'exp': datetime.datetime.utcnow() + datetime.timedelta(
                           minutes=int(app_sets.settings['JWT']['lifetime']))},
                      app_sets.settings['JWT']['key'], algorithm='HS256')
