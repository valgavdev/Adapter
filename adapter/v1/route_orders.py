import json
import string
import random
from typing import Optional

from fastapi import HTTPException

from fastapi import Depends

from . import router_v1
from ..api import models, baseadapter
from adapter import dependencies
import exceptionex
from ..api.ts94 import TS94
from ..exceptions import CardNotExist, PumpBusy


@router_v1.post("/payment", tags=['Заказы'], summary='Оформление заказа')
def payment(order: models.Order, ts94=Depends(dependencies.get_ts94)) -> models.Order:  # , user: str = Depends(dependencies.check_token)
    # adapter = baseadapter.BaseAdapter.create(order.pos.provider)
    # return adapter.payment(order)
    # if order.payInfo.identifier != '926088':
    #     raise CardNotExist()

    if order.columnId > 1:
        raise PumpBusy()
    order.orderId = ts94.payment(order)
    return order



@router_v1.post("/order_status", tags=['Заказы'], summary='Статус заказа')
def order_status(apikey: Optional[str] = None):
    return ''


def generate_random_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


