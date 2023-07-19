class BaseException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

        super().__init__(self.code, self.message)


class CardNotExist(BaseException):
    def __init__(self):
        super().__init__(101, 'Карта не найдена')


class CardInvalidNumber(BaseException):
    def __init__(self):
        super().__init__(102, 'Неверный номер карты')


class PumpBusy(BaseException):
    def __init__(self):
        super().__init__(2404, 'Колонка занята')


class StationOrPumpNotFound(BaseException):
    def __init__(self):
        super().__init__(2400, 'Неверный идентификатор станции или ТРК')


class PriceIncorrect(BaseException):
    def __init__(self):
        super().__init__(2402, 'Несоответсвие цены')


class NotConnected(BaseException):
    def __init__(self, text: str):
        super().__init__(503, f'Нет соединения c {text}')


class ExchangeError(BaseException):
    def __init__(self, text: str):
        super().__init__(2500, f'Ошибка обмена с {text}')


class TS94Exception(BaseException):
    def __init__(self, code: int, text: str):
        super().__init__(code + 1000, text)


class TransactionNotFound(BaseException):
    def __init__(self):
        super().__init__(171, 'Транзакция списания не найдена')


class NotFoundApikey(BaseException):
    def __init__(self):
        super().__init__(505, 'Не найден apikey')
