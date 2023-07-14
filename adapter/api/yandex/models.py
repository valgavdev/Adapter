from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum

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

@dataclass
class Order:
    Id: int 			    # идентификатор заказа !!!
    DateCreate: datetime    # дата и время создания в UTC
    OrderType: OrderType    # тип заказа
    OrderVolume: float      # значение заказа
    StationExtendedId: str  # внешний идентификатор станции АЗС
    ColumnId: int           # номер колонки
    PriceId: str            # идентификатор прайса
    FuelExtendedId: str     # внешний идентификатор прайса
    PriceFuel: float        # стоимость 1 литра топлива
    Sum: float              # сумма заказа
    Litre: float            # кол-во литров
    Status: OrderStatus     # статус заказ
    DateEnd: datetime       # дата и время завершения заказа UTC
    ReasonId: str           # идентификатор причины отмены заказа
    Reason: str             # причина отмены
    LitreCompleted: float   # итого сумма литров залито
    SumPaidCompleted: float # итого оплачено по завершению заказа
