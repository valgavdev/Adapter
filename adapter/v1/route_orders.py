from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from functools import partial

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
import json
from fastapi import Depends
import time
import dataset
from . import router_v1
from ..api import models, baseadapter
from adapter import dependencies

from ..api.yandex.models import OrderStatus
from ..exceptions import CardNotExist, PumpBusy, NotFoundApikey, TransactionNotFound, StationOrPumpNotFound
from ..logger import http_logger
from ..api.yandex import models as yandexmodels
import requests


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


def run_sync_code(task, *args, **kwargs):
    executor = ThreadPoolExecutor()
    loop = get_event_loop()
    loop.run_in_executor(executor, partial(task, *args, **kwargs))


@router_v1.post("/order_status/{status}", tags=['Заказы'], summary='Статус заказа', response_model_exclude_none=True)
@router_v1.post("/order_status/{rest_of_path:path}/{status}", tags=['Заказы'], summary='Статус заказа',
                response_model_exclude_none=True)
async def order_status(status: StatusType, orderId: Optional[str] = None,
                 rest_of_path: Optional[str] = None,
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
    order = None
    dt_end = None
    for row in ds_prov:
        provider = row.get('pos_provider')
        to_sts = row.get('to_sts')
        if to_sts:
            order = yandexmodels.Order.from_json(to_sts)

    if provider == -1:
        raise TransactionNotFound()

    adapter = baseadapter.BaseAdapter.create(provider, db, ts94)

    if status == StatusType.completed:
        # db.update_transaction(orderId, None, litre)
        # adapter.confirm(orderId, litre)

        order.Status = OrderStatus.Completed.name
        order.LitreCompleted = litre
        order.SumPaidCompleted = round(litre * order.PriceFuel, 2)
        order.DateEnd = datetime.now(timezone.utc).astimezone().isoformat()
        run_sync_code(adapter.send_order, order, True)
        # background_tasks.add_task(adapter.send_order, order, True)
        http_logger.info('method: order_status; before tasks')
        return

    if status == StatusType.accept:
        return
    if status == StatusType.canceled:
        db.update_transaction(orderId, reason, None)
        adapter.confirm(orderId, 0.00)
    return