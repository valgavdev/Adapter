from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import IntEnum
from typing import Optional

from enumex import IntEnumDesc


class OrderType(IntEnumDesc):
    Money       = (0, 'Заправка на фиксированную сумму, OrderVolume – сумма рублей')
    Liters      = (1, 'Заправка на литры, OrderVolume – кол-вол литров')
    FullTank    = (2, 'Полный бак, OrderVolume – максимальная сумма рублей')


class OrderStatus(IntEnumDesc):
    OrderCreated    = (0, 'Заказ создан и полностью оплачен')
    Expire          = (1, 'Статус от АЗС не поступил в течение 30 минут')
    Completed       = (2, 'Заказ завершен успешно')
    StationCanceled = (3, 'Заказ отменен оператором АЗС или же интегрируемой системой')
    UserCanceled    = (4, 'Заказ отменен пользователем')
# {
#     "Id": "5F99BF26-D980-41E6-912F-50DB7D9DF1D8",
#     "DateCreate": "2023-07-14T11:47:50.000Z",
#     "OrderType": "Liters",
#     "OrderVolume": 2.0,
#     "StationExtendedId": "190011",
#     "ColumnId": 1,
#     "FuelId": "a92",
#     "FuelMarka": "АИ-92",
#     "FuelExtendedId": "a92",
#     "PriceFuel": 50.0,
#     "Sum": 100.0,
#     "Litre": 2.0,
#     "Status": "OrderCreated"
# }

@dataclass_json
@dataclass
class Order:
    Id: Optional[str] = None 			    # идентификатор заказа !!!
    DateCreate: Optional[str] = None    # дата и время создания в UTC
    OrderType: Optional[str] = None    # тип заказа
    OrderVolume: Optional[float] = None      # значение заказа
    StationExtendedId: Optional[str] = None  # внешний идентификатор станции АЗС
    ColumnId: Optional[int] = None           # номер колонки
    FuelExtendedId: Optional[str] = None     # внешний идентификатор прайса
    PriceFuel: Optional[float] = None        # стоимость 1 литра топлива
    Sum: Optional[float] = None              # сумма заказа
    SumPaid: Optional[float] = None  # сумма заказа
    Litre: Optional[float] = None            # кол-во литров
    Status: Optional[str] = None     # статус заказ
    DateEnd: Optional[str] = None      # дата и время завершения заказа UTC
    ReasonId: Optional[str] = None           # идентификатор причины отмены заказа
    Reason: Optional[str] = None             # причина отмены
    LitreCompleted: Optional[float] = None   # итого сумма литров залито
    SumPaidCompleted: Optional[float] = None # итого оплачено по завершению заказа
