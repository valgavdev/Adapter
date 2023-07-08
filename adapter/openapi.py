#from tabulate import tabulate
from enum import IntEnum, Enum
from fastapi.openapi.utils import get_openapi
from dataclasses import dataclass

from enumex import IntEnumDesc


#from elsyplusapi import app_sets
#from common import enumex


@dataclass
class Descriptions:
    class FormatType(IntEnum):
        text        = 0
        code        = 1
        list_txt    = 2
        list_code   = 3

    @staticmethod
    # "..." - text
    # ("...", ...) - plain list
    # ["...", ...] - format list
    def build(*args, format: FormatType = FormatType.text) -> str:
        text = ''
        for line in args:
            if isinstance(line, list):
                text += Descriptions.build(*line, format=Descriptions.FormatType.list_code) + '\r\n'
            elif isinstance(line, tuple):
                text += Descriptions.build(*line, format=Descriptions.FormatType.list_txt) + '\r\n'
            elif isinstance(line, str):
                if line and len(line) > 0:
                    if format == Descriptions.FormatType.text:
                        # plain text
                        text = f'{text}{line}\r\n\r\n'
                    elif format == Descriptions.FormatType.code:
                        # format text
                        text = f'{text}\t{line}\r\n'
                    elif format == Descriptions.FormatType.list_txt:
                        # plain list
                        text = f'{text}- {line}\r\n'
                    elif format == Descriptions.FormatType.list_code:
                        # format list
                        text = f'{text}\t· {line}\r\n'

        return text

    @staticmethod
    def enum(enum) -> str:
        if issubclass(enum, IntEnumDesc):
            return Descriptions.build(*enum.descriptions(), format=Descriptions.FormatType.list_code)
        elif issubclass(enum, Enum):
            return Descriptions.build(*[f'{t.value} - {t.name}' for t in enum],
                                      format=Descriptions.FormatType.list_code)

    def __init__(self):
        self.dt = 'YYYY-MM-DD hh:mm:ss'
        self.dt_example = '2022-01-28 14:23:45'

        '''self.mode_update = self.build('**mode**:', '\tmode:', self.enum(DBModeUpdate),
                                                   '\terror - если = 1, метод возвращает ошибку в следующих ситуациях:',
                                      ['Задан режим вставки, но контрагент уже существует',
                                       'Задан режим редактирования, но контрагента не существует.'])
'''

descriptions = Descriptions()

_doc_description = ''

'''    
    f"""
## Список сокращений

**ПЦ** - процессинг.

**ТС** - топливный счет. Для каждого договора открывается свой ТС.

**КС** - карточный счет. Карта и КС взаимозаменяемые термины.

## Типы

**datetime** - дата/время: {descriptions.dt}

## Протокол

JSON RPC 2.0

## Начало работы

Для начала работы необходимо вызвать метод login, в который необходимо передать логин и пароль либо в заголовке, либо 
в параметрах метода. Для передачи в заголовке можно воспользоваться кнопкой Authorize и ввести логин и пароль в поля 
на форме (HTTPBasic  (http, Basic)).

В случае успешной авторизации клиенту будет возвращен JWT, который необходимо использовать для формирования всех 
запросов. JWT помещается в заголовок в поле «Authorization». Можно воспользоваться кнопкой Authorize и ввести JWT 
в поле на форме (HTTPBearer  (http, Bearer)). Время жизни JWT: **{app_sets.settings['JWT']['lifetime']}** минут. 

## Права доступа

Для каждой учетной записи выдаются разрешения (чтение, запись) для работы с определенным списком эмитентов. 
В каждый метод передается параметр **emitent**. Если передан код эмитента, для работы с которым учетной записи 
не выдано разрешение, то метод вернет ошибку.   

## Асинхронный режим

Часть методов работает в асинхронном режиме. У таких методов в описании присутсвует раздел **Callbacks**. 
После выполнения таких методов в адрес инициатора запроса (**{app_sets.get('RECEIVER', 'url', 'http://callback')}**) отправляется результат выполнения. 
В случае ошибки отправляется информация об ошибке.

## Задание условий

В некторые методы для фильтрации выходных данных можно передавать условия фильтрации. 
Условия имеют следующий вид:

    "имя_параметра": <условие>
    
**Условие**:

{tabulate([['equal', '[type]', 'Равенство'], 
           ['unequal', '[type]', 'Неравенство'],
           ['more', 'type', 'Больше'],
           ['less', 'type', 'Меньше']], 
          headers=['Имя', 'Тип', 'Описание'], tablefmt='html')}

Условия объединяются оператором **AND**:
	
	(x in equal) AND (x not in unequal) AND (x > more) AND (x < less)

Чтобы включить значение в границы диапазона для more/less необходимо заключить его в []:
    
    "more": [1000] -> x >= 1000

Для строковых данных возможно задать фильтрацию по части имени. Для этого используются символы:
 
    [%] - несколько любых символов
    [_] - один любой символ

Условия могут объединяться в списки. В этом случае к ним будет применен оператор OR.

**Примеры**:
    
    "id": [{{"equal": [1,2,3]}}]
        
        Метод вернет данные, у которых: id = 1, 2 или 3
        
    "dt": [{{"more": ["2022-01-01"], "less": "2022-02-01"}},
           {{"more": ["2022-04-01"], "less": "2022-05-01"}}]
    
        Метод вернет данные, у которых: (dt >= "2022-01-01" и dt < "2022-02-01") или (dt >= "2022-04-01" и dt < "2022-05-01")   
        
## Фильтры

Фильтры содержат условия по полям. Фильтр может быть json-объектом (1), массивом json-объектов (2) и массивом массивов json-объектов (3).

(1) Условия по полям внутри json-объекта объединяются оператором AND.

(2) Условия полученные из json-объектов объединяются оператором OR. Используется для создания условий типа: ((... AND ...) OR (... AND ...))

(3) Условия полученые из масивов json-объектов объединяются оператором AND. Используется для создания условий типа: ((... OR ...) AND (... OR ...))

**Примеры**:

(1)

    filter: {{
        "operation": [{{"equal": [1, 2, 3]}}],
        "dt": [{{"more": ["2022-01-01"]}}]    
    }}
   
Условие: 
    
    (operation IN (1, 2, 3)) AND (dt >= "2022-01-01")
    
(2)

    filter: [{{
        "operation": [{{"equal": [1, 2, 3]}}],
        "dt": [{{"more": ["2022-01-01"]}}]    
    }},
    {{
        "operation": [{{"more": [10]}}]
    }}]
    
Условие:
    
    ((operation IN (1, 2, 3)) AND (dt >= "2022-01-01")) OR (operation >= 10)
    
(3)

    filter: [[{{
        "operation": [{{"equal": [1, 2, 3]}}],
        "dt": [{{"more": ["2022-01-01"]}}]    
    }},
    {{
        "operation": [{{"more": [10]}}]
    }}],
    [{{
        "dt": [{{"less": "2023-01-01"}}]
    }}]]

Условие:

    (((operation IN (1, 2, 3)) AND (dt >= "2022-01-01")) OR (operation >= 10)) AND
    (dt < "2023-01-01")
"""
'''

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ADAPTER",
        version="1.0.0",
        routes=app.routes,
        description=_doc_description
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
