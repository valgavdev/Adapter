import json
import string
import random
from enum import Enum
from typing import Optional

from fastapi import HTTPException, Request

from fastapi import Depends

from . import router_v1
from ..api import models, baseadapter
from adapter import dependencies
import exceptionex
from ..api.ts94 import TS94
from ..exceptions import CardNotExist, PumpBusy
from ..logger import http_logger


@router_v1.post("/payment", tags=['Заказы'], summary='Оформление заказа')
def payment(order: models.Order,
            ts94=Depends(dependencies.get_ts94), db=Depends(dependencies.get_db)) -> models.Order:  # , user: str = Depends(dependencies.check_token)
    adapter = baseadapter.BaseAdapter.create(order.pos.provider, db, ts94)
    s = adapter.payment(order)
    # return adapter.payment(order)


    return order


# if order.columnId == 2:
#     raise PumpBusy()
#
# if not order.paid:
#     order.orderId = ts94.payment_confirm('payment', order)


class StatusType(str, Enum):
    accept = 'accept'
    canceled = 'canceled'
    fueling = 'fueling'
    completed = 'completed'
    bank_card_ticket = 'bank_card_ticket'


@router_v1.post("/order_status/{status}")
@router_v1.post("/order_status/{rest_of_path:path}/{status}", tags=['Заказы'], summary='Статус заказа')
def order_status(status: StatusType, rest_of_path: Optional[str] = None, apikey: Optional[str] = None,
                 orderId: Optional[str] = None, litre: Optional[float] = None, extendedOrderId: Optional[str] = None,
                 extendedDate: Optional[str] = None, reason: Optional[str] = None):
    # if status == StatusType.accept:
    if reason:
        http_logger.info(f'reason:{reason}')
    return


def generate_random_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
