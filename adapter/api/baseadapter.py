from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List

from fastapi import Depends

import dataset
from . import models
from .models import ProviderType
from .yandex.protocol import YandexApi
from .. import dependencies


class BaseAdapter(ABC):
    @staticmethod
    def get_provider_info(provider: int, db=Depends(dependencies.get_db)) -> List[models.ProviderInfo]:
        prov = db.provider_info(provider)

        ds_prov = dataset.DataSet(description=prov.statement.subquery().columns.keys(),
                                  data=[v.as_dict() for v in prov.all()])
        json = {'id': 'id', 'name': 'name'}
        print(ds_prov.format([], json))
        return ds_prov.format([], json)

    @staticmethod
    def create(type: int) -> 'BaseAdapter':
        if (type == ProviderType.Yandex.value):
            from .yandexadapter import YandexAdapter
            return YandexAdapter()
        raise Exception('No Api')

    @abstractmethod
    def payment(self, orders: models.Order):
        pass
