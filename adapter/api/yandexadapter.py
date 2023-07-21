import http
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional
import time
from fastapi import Depends

import dataset
from . import models, baseadapter
from .models import OrderType, ProviderInfo
from .yandex import models as yandexmodels
from .yandex.models import OrderStatus, OrderType
from .yandex.protocol import YandexApi
import requests

from .. import dependencies
from ..exceptions import PumpBusy, StationOrPumpNotFound, ExchangeError
from ..logger import http_logger


class YandexAdapter(baseadapter.BaseAdapter):
    def __init__(self, provider_info: ProviderInfo, ts94=Depends(dependencies.get_ts94),
                 db=Depends(dependencies.get_db)):
        data = json.loads(provider_info.connection_info.replace('\'', '"'))
        self.__url = data['url']
        if self.__url[-1] != '/': self.__url += '/'
        self.__apikey = data['key']
        self.__ts94 = ts94
        self.__db = db

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

        yandexOrder = self.convert_to(OrderStatus.OrderCreated, orders)

        # json = asdict(yandexOrder)
        # s= json.dumps(asdict(yandexOrder))
        self.__db.insert_transaction(orders, json.dumps(asdict(yandexOrder)))

        if not self.send_order(yandexOrder):
            raise ExchangeError('STS')
        return orders

    def confirm(self, orderId: str, sumpaid: float):
        trans = self.__db.get_transactions(orderId)

        sum = int(sumpaid * 100.0)

        ds_trans = dataset.DataSet(description=trans.statement.subquery().columns.keys(),
                                   data=[v.as_dict() for v in trans.all()])
        for row in ds_trans:
            order = models.Order(orderId=orderId, amount=sum, columnId=row.get('column_id'),
                                 payInfo=models.Order.PayInfo(emitent=row.get('pay_info_emitent'),
                                                              identifier=row.get('pay_info_identifier')),
                                 pos=models.Order.Pos(identifier=row.get('pos_identifier'),
                                                      provider=row.get('pos_provider')),
                                 price=row.get('price'), serviceId=row.get('goods_ext_id'),
                                 type=row.get('order_type'), typePlat=row.get('type_plat'), paid=row.get('paid'),
                                 date=row.get('dt_beg'))

        res = self.__ts94.payment_confirm('payment_confirm', order)

    def send_order(self, ya: yandexmodels.Order, is_time: bool = False) -> bool:
        prepare = asdict(ya, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
        http_logger.info(f'method: send_order; request: {prepare}')
        if is_time:
            time.sleep(2)
            http_logger.info(f'method: send_order; is_time')
        #response = requests.post(f"{self.__url}order", data=json.dumps(prepare), params={'apikey': self.__apikey})
        response = requests.post(f"http://localhost:6952/OnlineService.asmx/tresp", data=json.dumps(prepare))
        http_logger.info(f'method: send_order; response: {response.status_code}')
        if response.status_code == 404:
            raise PumpBusy()
        if response.status_code == 400:
            raise StationOrPumpNotFound()
        # response.raise_for_status()
        if response.status_code == 200:
            return True
        else:
            return False

    def convert_to(self, status: OrderStatus, orders: models.Order) -> yandexmodels.Order:

        yandex = yandexmodels.Order(Id=orders.orderId,
                                    DateCreate=orders.date.isoformat(),
                                    OrderType=OrderType(orders.type).name,
                                    OrderVolume=orders.amount / 100.0,
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
        yandex.SumPaid = yandex.Sum
        return yandex

        # return self.send_order(json.dumps(yandex.__dict__))
