from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List, Optional

from fastapi import Depends

import dataset
from . import models
from .models import ProviderType, ProviderInfo
from .yandex.protocol import YandexApi
from .. import dependencies
from ..api.yandex import models as yandexmodels
from ..db.worker import Worker


def get_provider_info(provider: int, db: Depends(dependencies.get_db)) -> ProviderInfo:
    # db = Worker()
    prov = db.provider_info(provider)

    ds_prov = dataset.DataSet(description=prov.statement.subquery().columns.keys(),
                              data=[v.as_dict() for v in prov.all()])
    for row in ds_prov:
        provider_info = ProviderInfo(id=row.get('id'), type=row.get('type'), provider_name=row.get('provider_name'),
                                     provider_type_name=row.get('provider_type_name'),
                                     connection_info=row.get('connection_info'))
    return provider_info


class BaseAdapter(ABC):
    @staticmethod
    def create(type: int, db: Depends(dependencies.get_db), ts94=Depends(dependencies.get_ts94),
               provider_type: Optional[int] = None) -> 'BaseAdapter':
        if not provider_type:
            provider_info = get_provider_info(type, db)
        if (provider_info.type == ProviderType.Yandex.value):
            from .yandexadapter import YandexAdapter
            return YandexAdapter(provider_info, ts94, db)
        raise Exception('No Api')

    @abstractmethod
    def payment(self, orders: models.Order):
        pass

    @abstractmethod
    def confirm(self, orderId: str, amount: float):
        pass

    @abstractmethod
    def send_order(self, ya: yandexmodels.Order, is_time: bool = False):
        pass