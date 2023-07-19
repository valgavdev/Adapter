from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

import uvicorn

from adapter.db.worker import Worker
from adapter.main import app
from enumex import IntEnumDesc


uvicorn.run(app, host="0.0.0.0", port=5000)


# @dataclass
# class Order:
#     Id: str 			    # идентификатор заказа !!!
#     DateCreate: datetime    # дата и время создания в UTC
#     OrderType: str    # тип заказа
#     DateEnd: Optional[datetime] = None      # дата и время завершения заказа UTC
#     ReasonId: Optional[str] = None           # идентификатор причины отмены заказа
#     SumPaidCompleted: Optional[float] = None # итого оплачено по завершению заказа

# class OrderType(IntEnumDesc):
#     Money       = (0, 'Заправка на фиксированную сумму, OrderVolume – сумма рублей')
#     Liters      = (1, 'Заправка на литры, OrderVolume – кол-вол литров')
#     FullTank    = (2, 'Полный бак, OrderVolume – максимальная сумма рублей')
#
# @dataclass
# class Test:
#     gaga: OrderType
#

# print(asdict(t))


# ty: int = 0
# order_amount: int = 47340
# order_price: int = 5000
#
# sum: float
# litres: float
#
# s:float = order_amount / order_price
# if ty == 0:
#     litres = float(order_amount / order_price) / 100



#orderType = 1
#t:str = OrderType(orderType).name
# from sqlalchemy.orm import create_session
# from sqlalchemy import create_engine, Column, Integer
# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy.schema import Table, MetaData
#
# # from sqlalchemy_views import CreateView
#
# engine = create_engine("postgresql+psycopg2://postgres:sys5tem6@127.0.0.1/adapterpc")
# session = create_session(bind=engine)
# Base = declarative_base()
# metadata = MetaData()
# metadata.reflect(bind=engine)
#
#
# class DBTransactions(Base):
#     __table__ = Table('transaction', metadata, autoload=True)
#
# t = DBTransactions()
# t.order_id = 'dgfg'
#
#
# session.add(t)
# session.commit()
#with session.begin() as s:
#    s.add(t)


#db = orker.Worker()
# q = db.stations(3)
#
# prov = db.providers()
# prov2 = db.providers2()
# ds_prov = dataset.DataSet(description=prov2.statement.subquery().columns.keys(),
#                           data=[v.as_dict() for v in prov2.all()])
# json = {'id': 'id', 'name': 'name'}
# print(ds_prov.format([], json))
#
#
#
#
#
# qprices = db.prices()
# ds_prices = dataset.DataSet(description=qprices.statement.subquery().columns.keys(),
#                             data=[v.as_dict() for v in qprices.all()])
# prices = ds_prices.groupby('station_id', {'serviceId': 'goods_id', 'price': 'price'})
#
#
# def get_value(field, row, row_index):
#     if field == 'prices' and prices:
#         return prices.get(row['station_id'])
#
#     return None
#
#
# ds = dataset.DataSet(description=q.statement.subquery().columns.keys(),
#                      data=[v.as_dict() for v in q.all()])
# res = ds.format(['station_id', 'pump'],
#                 {
#                     'pumps': [{
#                         'fuels': [{
#                             'serviceId': 'goods_id',
#                             'name': 'shortname'
#                         }],
#                         'number': 'pump'
#                     }],
#                     'id': 'station_id',
#                     'prices': '()'
#                 },
#                 get_value=get_value)
# print(res)

#
# class Station(Base):
#     __table__ = Table('station', metadata, autoload=True)
#
#
# class ViewT(Base):
#     __table__ = Table('_vw_stations_config', metadata, Column("id", Integer, primary_key=True), autoload=True)
#
#
# viewStationConfig = Table('_vw_stations_config', metadata, autoload_with=engine)

# stationList = session.query(ViewT).all()
# print(stationList[0])
# ds = dataset.DataSet(description=list(stat[0].keys())),
#                                  data=[list(row.values()) for row in json])
# for station in stationList:
#     print("id: {}; station: {}; price: {}".format(station.station_id, station.station, station.price))
# print(station)

# create_view = CreateView('testview', t.select)
# engine.execute(create_view)

# session = create_session(bind=engine)
#
# stationList = session.query(Station).all()
# for station in stationList:
#     print("id: {}; station: {}; price: {}".format(station.id, station.name, station.price))

# import psycopg2
#
# v_name: str = 'gaga8'
#
# conn = psycopg2.connect(database="AdapterPC", user="postgres", password="sys5tem6", host="10.10.33.111", port="5432")
# cur = conn.cursor()
# #cur.execute('CALL _sp_test_ins(v_name=>\"{v_name}\")'.format(v_name=v_name))
# sql = 'CALL _sp_test_ins(v_name => {})'.format(v_name)
# cur.execute(sql)
# result_set = cur.fetchall()
# conn.commit()
# cur.close()
# conn.close()

# import postgesqldb as db
# connectInfo = db.ConnectionInfo(server='127.0.0.1', dbname='AdapterPC', user='postgres', password='sys5tem6', port=5432)
# conn = db.PostgerSQLDB()
# conn.set_connection_info([connectInfo])
# conn.connect()
# #ds = conn.open_table('public.GOODS')
# v_name = 'gaga7'
# #conn.exec_sp('public._sp_test_ins', [db.ParamSP('v_name', v_name)])
# param = 'call public._sp_test_ins({v_name})'.format(v_name = v_name)
# ds = conn.exec_sp('public._sp_test_ins', [db.ParamSP('v_name', v_name)])
#
# for row in ds:
#     row.get('name')

# json = {'id': 'Id', 'name': 'Name'}
# print(ds.format([], json))
#
# for row in ds:
#     row.get('Name')

'''
def func() -> List[GOODS]:
    return ds.format([], json)


class GOODS(BaseModel):
    id: int
    nmae: str
'''
