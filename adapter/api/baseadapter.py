from abc import ABC, abstractmethod
from enum import IntEnum

from . import models
from .models import ProviderType
from .yandex.protocol import YandexApi


class BaseAdapter(ABC):
    @staticmethod
    def create(type: int) -> 'BaseAdapter':
        if (type == ProviderType.Yandex.value):
            from .yandexadapter import YandexAdapter
            return YandexAdapter()
        raise Exception('No Api')

    @abstractmethod
    def payment(self, orders: models.Order):
        pass
