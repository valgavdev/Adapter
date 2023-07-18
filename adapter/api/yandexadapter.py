import http
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from fastapi import Depends

from . import models, baseadapter
from .models import OrderType, ProviderInfo
from .yandex import models as yandexmodels
from .yandex.models import OrderStatus, OrderType
from .yandex.protocol import YandexApi
import requests

from .. import dependencies
from ..exceptions import PumpBusy, StationOrPumpNotFound


class YandexAdapter(baseadapter.BaseAdapter):
    def __init__(self, provider_info: ProviderInfo, ts94=Depends(dependencies.get_ts94)):
        data = json.loads(provider_info.connection_info.replace('\'', '"'))
        self.__url = data['url']
        if self.__url[-1] != '/': self.__url += '/'
        self.__apikey = data['key']
        self.__ts94 = ts94

    def ping(self, stationId: str, columnId: int) -> bool:
        params = {'apikey': self.__apikey, 'stationId': stationId, 'columnId': columnId}

        response = requests.get(f"{self.__url}ping", params=params)

        if response.status_code == 200:
            return True
        else:
            return False

    def payment(self, orders: models.Order) -> models.Order:
        if not self.ping(orders.pos.identifier, orders.columnId):
            raise PumpBusy()

        orders.orderId = self.__ts94.payment_confirm('payment', orders)

        # конвертипм наш models.Order в order yandex
        ya = self.convert_to(OrderStatus.OrderCreated, orders)

        self.send_order(ya)

        api = YandexApi()
        res = api.payment(ya)
        # конвертим res в ответ для мобильного
        pass

    def send_order(self, ya: yandexmodels.Order) -> str:
        response = requests.post(f"{self.__url}order", json=asdict(ya),
                                 params={'apikey': self.__apikey})

        if response.status_code == 404:
            raise PumpBusy()
        if response.status_code == 400:
            raise StationOrPumpNotFound()
        response.raise_for_status()
        return response.json()

    def convert_to(self, status: OrderStatus, orders: models.Order) -> yandexmodels.Order:

        yandex = yandexmodels.Order(Id=orders.orderId,
                                    DateCreate=orders.date.isoformat(),
                                    OrderType=OrderStatus(orders.type).name,
                                    OrderVolume=orders.amount,
                                    StationExtendedId=orders.pos.identifier,
                                    ColumnId=orders.columnId,
                                    FuelExtendedId=orders.serviceId,
                                    Status=status.name,
                                    PriceFuel=0.00,
                                    Sum=0.00,
                                    Litre=0.00)

        yandex.PriceFuel = float(orders.price) / 100
        if orders.type == OrderType.Money:
            yandex.Sum = float(orders.amount) / 100
            yandex.Litre = round(yandex.Sum / yandex.PriceFuel, 2)
        else:
            yandex.Litre = float(orders.amount) / 100
            yandex.Sum = round(float(orders.price * orders.amount) / 10000, 2)

        return yandex

        # return self.send_order(json.dumps(yandex.__dict__))
