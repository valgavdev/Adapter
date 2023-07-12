import json
import string
import random
from typing import Optional

from fastapi import HTTPException, Request

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

    if order.columnId == 2:
        raise PumpBusy()

    if not order.paid:
        order.orderId = ts94.payment_confirm('payment', order)

    return order



@router_v1.post("/order_status", tags=['Заказы'], summary='Статус заказа')
async def order_status(request: Request, apikey: Optional[str] = None):
    s ='gaga'
    resp = await request.body()

    return ''


def generate_random_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


