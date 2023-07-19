from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from adapter import openapi
from enumex import IntEnumDesc


@dataclass
class Fuel:
    serviceId: int = Field(..., title='Идентификатор услуги')
    serviceExtId: str = Field(..., title='Идентификатор внешней услуги')
    name: str = Field(..., title='Наименование услуги')


@dataclass
class Pump:
    fuels: List[str] = Field(..., title='Список доступных видов н/п на колонке')
    number: int = Field(..., title='Номер колонки')


@dataclass
class Price:
    id: int = Field(..., title='Идентификатор услуги')
    extId: str = Field(..., title='Внешний идентификатор услуги')
    name: str = Field(..., title='Наименование услуги')
    price: float = Field(..., title='Цена услуги за еденицу')


@dataclass
class StationInfo:
    pumps: List[Pump] = Field([], title='Список колонок')
    provider: int = Field(..., title='Идентификатор системы управления АЗС')
    id: str = Field(..., title='Идентификатор АЗС')
    services: List[Price] = Field([], title='Список услуг')
    name: str = Field(..., title='Наименование')
    address: str = Field(..., title='Адрес')
    longitude: Optional[str] = Field(None, title='Долгота')
    latitude: Optional[str] = Field(None, title='Широта')


class Book(BaseModel):
    id: int = Field(..., title='Идентификатор')
    name: str = Field(..., title='Наименовние')


@dataclass
class ProviderInfo:
    id: int
    type: int
    provider_name: str
    provider_type_name: str
    connection_info: str


class MapGoods(BaseModel):
    provider: int = Field(..., title='Идентификатор провайдера')
    goods: int = Field(..., title='Идентификатор услуги локальный')
    goods_ex: str = Field(..., title='Идентификатор услуги сторонний')


class Errors:
    def __init__(self, code: int, errorText: str):
        self.code: int
        self.errorText: Optional[str] = None


class Errors2:
    code: int
    errorText: Optional[str] = None


class OrderType(IntEnumDesc):
    Money = (0, 'Заправка на фиксированную сумму')
    Liters = (1, 'Заправка на литры')
    # FullTank = (2, 'Полный бак, OrderVolume – максимальная сумма рублей')


# у провайдеров с разным кодом может быть один тип
class ProviderType(IntEnumDesc):  # тип провайдера
    Yandex = (1, 'Yandex')


# class ProviderType(IntEnumDesc):  # код провайдера
#    InvoiceBox = (1, 'Инвойсбокс')


class TypePlat(IntEnumDesc):
    Column = (0, 'У колонки')
    Operator = (1, 'У оператора')


class Order(BaseModel):
    class PayInfo(BaseModel):
        emitent: int = Field(...,
                             title='Идентификатор процессинга для финансовых расчетов')  # идентификатор процессинга для финансовых расчетов (Леонид, Инвойсбокс) ||||   1
        identifier: str = Field(...,
                                title='Идентификатор платежа (номер карты)')  # идентификатор платежа (номер карты) (с чего списываем (банковская, куэр))

    class Pos(BaseModel):
        provider: int = Field(..., title='Идентификатор системы управления АЗС',
                              description=openapi.descriptions.enum(
                                  ProviderType))  # идентификатор системы управления АЗС   ПО POS ПРОВАЙДЕРА Инвойсбокс
        identifier: str = Field(..., title='Идентификатор АЗС')  # идентификатор pos

    payInfo: Optional[PayInfo]
    pos: Pos
    orderId: Optional[str] = Field(None, title='Идентификатор заказа')
    date: datetime = Field(..., title='Дата и время создания в UTC')
    type: OrderType = Field(..., title='Тип заказа', description=openapi.descriptions.enum(OrderType))
    columnId: int = Field(..., title='Номер колонки')
    serviceId: str = Field(..., title='Идентификатор услуги')
    price: int = Field(..., title='Цена')
    # cost: float             = Field(..., title='Сумма заказа')
    amount: int = Field(..., title='Кол-во услуги')
    typePlat: TypePlat = Field(..., title='Тип оплаты', description=openapi.descriptions.enum(TypePlat))
    paid: bool = Field(..., title='Заказ оплачен?')
    # errors: Errors2
