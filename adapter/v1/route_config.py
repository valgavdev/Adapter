from typing import Optional, List
from fastapi import Depends

import dataset
from . import router_v1
from .. import dependencies
from adapter.api import models


@router_v1.get("/stations", tags=['Конфигурация'], summary='Получение списка АЗС с ценами')
def get_config(pos: Optional[str] = None, provider: Optional[str] = None,
               db=Depends(dependencies.get_db)) -> List[models.StationInfo]:  # , user: str = Depends(dependencies.check_token)):
    # db = worker.Worker()

    qconfig = db.stations(pos, provider)
    qprices = db.prices()
    ds_prices = dataset.DataSet(description=qprices.statement.subquery().columns.keys(),
                                data=[v.as_dict() for v in qprices.all()])
    prices = ds_prices.groupby('station_id',
                               {'id': 'goods_id', 'extId': 'goods_ext_id', 'name': 'shortname',
                                'price': 'price'})

    def get_value(field, row, row_index):
        if field == 'services' and prices:
            return prices.get(row['station_id'])

        return None

    ds_config = dataset.DataSet(description=qconfig.statement.subquery().columns.keys(),
                                data=[v.as_dict() for v in qconfig.all()])
    res = ds_config.format(['station_id', 'pump'],
                           {
                               'pumps': [{
                                   'fuels': ['goods_ext_id'],
                                   'number': 'pump'
                               }],
                               'provider': 'provider',
                               'id': 'station',
                               'name': 'name',
                               'address': 'address',
                               'longitude': 'longitude',
                               'latitude': 'latitude',
                               'services': '()'
                           },
                           get_value=get_value)
    # print(res)
    return res


@router_v1.get("/providers", tags=['Конфигурация'], summary='Получение списка провайдеров')
# def get_providers(db=Depends(dependencies.get_db), user: str = Depends(dependencies.check_token)) -> List[models.Book]:
def get_providers(db=Depends(dependencies.get_db)) -> List[models.Book]:
    # db = worker.Worker()
    prov = db.providers()

    ds_prov = dataset.DataSet(description=prov.statement.subquery().columns.keys(),
                              data=[v.as_dict() for v in prov.all()])
    json = {'id': 'id', 'name': 'name'}
    print(ds_prov.format([], json))
    return ds_prov.format([], json)


@router_v1.get("/mapping/goods", tags=['Конфигурация'], summary='Маппинг кодов н/п')
def get_mapping_goods(provider: Optional[int] = None, db=Depends(dependencies.get_db)) -> List[models.MapGoods]:
    map_goods = db.map_goods(provider)

    ds_prov = dataset.DataSet(description=map_goods.statement.subquery().columns.keys(),
                              data=[v.as_dict() for v in map_goods.all()])
    json = {'provider': 'provider', 'goods': 'goods_id', 'goods_ex': 'goods'}

    return ds_prov.format([], json)
