import json
from dataclasses import dataclass, asdict
import uuid
from typing import Optional
from ..logger import http_logger

from . import models
# from .models import Payment, OrderInfo
from ..exceptions import NotConnected
from .. import jsonrpcclient


@dataclass
class ConnectionInfo:
    url: str
    login: str
    password: str


@dataclass
class Pos:
    identifier: str


@dataclass
class Service:
    identifier: str


@dataclass
class OrderInfo:
    service: Service
    price: int
    quantity: Optional[int] = None
    cost: Optional[int] = None


@dataclass
class Deal:
    emitent: int
    provider: int
    POS: Pos
    card: Optional[str] = None
    order: Optional[OrderInfo] = None
    payment_id: Optional[str] = None


class TS94(object):
    def __init__(self, connection_info: ConnectionInfo):
        if not connection_info:
            raise NotConnected('TS94')
        self.__client = jsonrpcclient.JSONRPCClient(connection_info.url)
        self.__login = connection_info.login
        self.__password = connection_info.password
        self.__JWT = self.__auth()

    def __headers(self) -> dict:
        return {'Authorization': f'Bearer {self.__JWT}'}

    def __auth(self) -> str:
        response = self.__client.exec('login', str(uuid.uuid4()), version='v1',
                                      params={'username': self.__login, 'password': self.__password})
        return response['result']

    def payment(self, order: models.Order):
        ord: OrderInfo = OrderInfo(service=Service(order.serviceId), price=order.price)
        if order.type == models.OrderType.Money:
            ord.cost = order.amount
        else:
            ord.quantity = order.amount

        payment = Deal(
            emitent=order.payInfo.emitent,
            card=order.payInfo.identifier,
            provider=order.pos.provider,
            POS=Pos(
                order.pos.identifier
            ), order=ord)

        http_logger.info(f'payment:{asdict(payment)}')

        response = self.__client.exec('payment', str(uuid.uuid4()), version='v1', header=self.__headers(),
                                      params=asdict(payment))

        http_logger.info(f'response: {response}')
        return response['result']

    def confirm(self, order: models.Order):
        confirm = Deal(
            emitent=order.payInfo.emitent,
            provider=order.pos.provider,
            POS=Pos(
                order.pos.identifier
            ), payment_id=order.orderId)

        http_logger.info(f'confirm:{asdict(confirm)}')

        response = self.__client.exec('payment_confirm', str(uuid.uuid4()), version='v1', header=self.__headers(),
                                      params=asdict(confirm))

        http_logger.info(f'response: {response}')
        return response['result']

    def cancel(self, order: models.Order):
        pass
