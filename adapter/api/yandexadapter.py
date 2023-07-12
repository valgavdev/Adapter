import json

from . import models, baseadapter
from .models import OrderType
from .yandex import models as yandexmodels
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

    def convert_to(self, orders: models.Order) -> yandexmodels.Order:
        yandex = yandexmodels.Order
        yandex.Id = 'генерим сами'
        yandex.DateCreate = orders.date
        yandex.OrderType = orders.type
        yandex.OrderVolume = orders.amount
        yandex.StationId = orders.pos
        yandex.StationExtendedId = orders.pos
        yandex.ColumnId = orders.columnId
        yandex.FuelId = orders.serviceId
        yandex.FuelMarka = orders.serviceId
        yandex.PriceId = ""
        yandex.FuelExtendedId = orders.serviceId
        yandex.PinCode = 0
        yandex.PriceFuel = orders.price
        yandex.Sum = orders.amount
        yandex.Litre = orders.amount
        yandex.SumPaidCoupon = 0.0
        yandex.SumPaidCard = 0.0
        yandex.SumPaid = 0.0
        yandex.Status = 0
        yandex.DateEnd = '0001-01-01T00:00:00'
        yandex.ReasonId = None
        yandex.Reason = None
        yandex.LitreCompleted = 0.0
        yandex.SumPaidCouponCompleted = 0.0
        yandex.SumPaidCardCompleted = 0.0
        yandex.SumPaidCompleted = 0.0
        yandex.PaymentId = 0
        yandex.TerminalKey = None
        yandex.UserEmail = ''
        yandex.UserPhone = ''
        yandex.DiscountStationPercent = 0.0
        yandex.DiscountStationPercentCompleted = 0.0
        yandex.DiscountStationSumPaid = 0.0
        yandex.DiscountStationSumPaidCompleted = 0.0
        yandex.ContractId = None

        return self.send_order(json.dumps(yandex.__dict__))


