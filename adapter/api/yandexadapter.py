import json

from . import models, baseadapter
from .models import OrderType
from .yandex import models as yandexmodels
from .yandex.models import OrderStatus, OrderType
from .yandex.protocol import YandexApi
import requests

from ..exceptions import PumpBusy, StationOrPumpNotFound


class YandexAdapter(baseadapter.BaseAdapter):
    def payment(self, orders: models.Order) -> models.Order:
        # конвертипм наш models.Order в order yandex
        yandexOrder = self.convert_to(orders)
        api = YandexApi()
        res = api.payment(yandexOrder)
        # конвертим res в ответ для мобильного
        pass

    def send_order(self, json: str) -> str:
        response = requests.post('http://integrator.tap365.ru:3000/tanker/order', json= json,
                                 params={'apikey': 'v4uam9kc4zsrps71v3p7gkg7'})

        if response.status_code == 404:
            raise PumpBusy()
        if response.status_code == 400:
            raise StationOrPumpNotFound()
        response.raise_for_status()
        return response.json()

    def convert_to(self, status: OrderStatus, orders: models.Order) -> yandexmodels.Order:
        yandex = yandexmodels.Order
        yandex.Id = orders.orderId
        yandex.DateCreate = orders.date
        yandex.OrderType = OrderStatus(orders.type).name
        yandex.OrderVolume = orders.amount
        yandex.StationExtendedId = orders.pos
        yandex.ColumnId = orders.columnId
        yandex.PriceId = ""
        yandex.FuelExtendedId = orders.serviceId
        yandex.PriceFuel = orders.price
        yandex.Sum = orders.amount
        yandex.Litre = orders.amount
        yandex.Status = status.name

        return self.send_order(json.dumps(yandex.__dict__))


