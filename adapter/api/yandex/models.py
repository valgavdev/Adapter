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


@dataclass
class Order:
    Id: int 			    # идентификатор заказа !!!
    DateCreate: datetime    # дата и время создания в UTC
    OrderType: OrderType    # тип заказа
    OrderVolume: float      # значение заказа
    StationId: str          # идентификатор станции АЗС
    StationExtendedId: str  # внешний идентификатор станции АЗС
    ColumnId: int           # номер колонки
    FuelId: str             # идентификатор топлива
    FuelMarka: str          # наименование марки топлива
    PriceId: str            # идентификатор прайса
    FuelExtendedId: str     # внешний идентификатор прайса
    PriceFuel: float        # стоимость 1 литра топлива
    Sum: float              # сумма заказа
    Litre: float            # кол-во литров
    SumPaid: float          # итого оплачено
    Status: OrderStatus     # статус заказ
    DateEnd: datetime       # дата и время завершения заказа UTC
    ReasonId: str           # идентификатор причины отмены заказа
    Reason: str             # причина отмены
    LitreCompleted: float   # итого сумма литров залито
    SumPaidCompleted: float # итого оплачено по завершению заказа
    ContractId: str         # идентификатор договора