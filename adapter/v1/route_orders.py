import json
import string
import random
from enum import Enum
from typing import Optional

from fastapi import HTTPException, Request

from fastapi import Depends

import dataset
from . import router_v1
from ..api import models, baseadapter
from adapter import dependencies
import exceptionex
from ..api.ts94 import TS94
from ..exceptions import CardNotExist, PumpBusy, NotFoundApikey, TransactionNotFound
from ..logger import http_logger


@router_v1.post("/payment", tags=['Заказы'], summary='Оформление заказа')
def payment(order: models.Order,
            ts94=Depends(dependencies.get_ts94),
            db=Depends(dependencies.get_db)) -> models.Order:  # , user: str = Depends(dependencies.check_token)
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


@router_v1.post("/order_status/{status}", tags=['Заказы'], summary='Статус заказа')
@router_v1.post("/order_status/{rest_of_path:path}/{status}", tags=['Заказы'], summary='Статус заказа')
def order_status(status: StatusType, orderId: Optional[str] = None, rest_of_path: Optional[str] = None,
                 apikey: Optional[str] = None,
                 litre: Optional[float] = None, extendedOrderId: Optional[str] = None,
                 extendedDate: Optional[str] = None, reason: Optional[str] = None, ts94=Depends(dependencies.get_ts94),
                 db=Depends(dependencies.get_db)):
    if not apikey:
        raise NotFoundApikey()

    prov = db.get_transactions(orderId)

    ds_prov = dataset.DataSet(description=prov.statement.subquery().columns.keys(),
                              data=[v.as_dict() for v in prov.all()])
    provider = -1
    for row in ds_prov:
        provider = row.get('pos_provider')
    if provider == -1:
        raise TransactionNotFound()

    adapter = baseadapter.BaseAdapter.create(provider, db, ts94)

    if status == StatusType.completed:
        db.update_transaction(orderId, None, litre)
        adapter.confirm(orderId, litre)
    if status == StatusType.accept:
        return
    if status == StatusType.canceled:
        db.update_transaction(orderId, reason, None)
        #adapter.confirm(orderId, 0.00)
    return
