from typing import Optional

import requests
import json

from .exceptions import TS94Exception, CardNotExist


class JSONRPCClient(object):
    def __init__(self, url):
        self.__url = url
        if self.__url[-1] != '/': self.__url += '/'

    def __create_body(self, method: str, rpc_id, **kwargs):
        return {'jsonrpc': '2.0',
                'method': method,
                'params': {k: v for k, v in kwargs.items() if v is not None},
                'id': rpc_id}

    def exec(self, method, rpc_id, header: Optional[dict] = {}, version: str = '', params: dict = {}) -> dict:
        header.update({'Content-Type': 'application/json; indent=4'})
        answ = requests.post(f'{self.__url}{version}', headers=header,
                             data=json.dumps(self.__create_body(method, rpc_id, **params)),
                             timeout=30, verify=False)
        self.__raise_for_status(answ)

        return answ.json()  # комментирую. Надо разбираться. В это месте может генерится exception, что не совсем правильно,
        # т. к. начинает спамиться клиент
        # Exception: Unexpected utf-8 bom

    def __raise_for_status(self, answ):
        answ.raise_for_status()
        json_err = answ.json().get('error')
        if json_err:
            raise TS94Exception(json_err['code'], json_err['message'])
