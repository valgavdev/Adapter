from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import create_session
from sqlalchemy import and_
from sqlalchemy.schema import Table, MetaData, Column
from ..api import models

from . import db_engine, Provider, Price, Vw, MapGoods, ProviderInfo, Transactions, Base, metadata, Apikey


class Worker(object):
    def __init__(self):
        self.__session = create_session(bind=db_engine)
        self.__provider = None

    def close(self):
        self.__session.close()

    # def providers2(self) -> List[Provider]:
    #     return self.__session.query(Provider.id, Provider.name).filter(Provider.type.is_not(None)).all()

    def providers(self):
        return self.__session.query(Provider).order_by(Provider.id)

    def provider_info(self, provider: Optional[int] = None):
        query = self.__session.query(ProviderInfo).order_by(ProviderInfo.id)
        if provider:
            return query.filter(ProviderInfo.id == provider)
        return query

    def map_goods(self, provider: Optional[int] = None):
        query = self.__session.query(MapGoods).order_by(MapGoods.provider, MapGoods.goods_id)
        if provider:
            return query.filter(MapGoods.provider == provider)
        return query

    def stations(self, station_id: Optional[str] = None, provider: Optional[int] = None):
        cond = None
        if station_id:
            cond = and_(Vw.provider == provider, Vw.station == station_id)
        else:
            cond = (Vw.provider == provider)

        query = self.__session.query(Vw).order_by(Vw.station, Vw.pump).filter(cond)
        print(str(query.statement.compile(dialect=postgresql.dialect())))

        return query

    def prices(self):
        return self.__session.query(Price)

    def apikey(self, key: str):
        return self.__session.query(Apikey).filter(Apikey.key == key)

    def get_transactions(self, orderId: str):
        return self.__session.query(Transactions).order_by(Transactions.id).filter(Transactions.order_id == orderId)

    def insert_transaction(self, order: models.Order, json: str):
        trans = Transactions()
        trans.order_id = order.orderId
        trans.pay_info_emitent = order.payInfo.emitent
        trans.pay_info_identifier = order.payInfo.identifier
        trans.pos_identifier = order.pos.identifier
        trans.pos_provider = order.pos.provider
        trans.amount = order.amount
        # trans.amount_completed = order
        trans.price = order.price
        trans.goods_ext_id = order.serviceId
        trans.order_type = order.type
        trans.type_plat = order.typePlat
        trans.paid = order.paid
        trans.dt_beg = order.date
        trans.column_id = order.columnId
        trans.to_sts = json
        # trans.dt_end =
        # trans.time_end = order.date
        # trans.reason
        self.__session.add(trans)
        self.__session.commit()

    def update_transaction(self, orderId: str, reason: Optional[str] = None, litre: Optional[float] = None,
                           yandex_order: Optional[str] = None):
        trans = Transactions()
        trans.order_id = orderId
        if reason:
            trans.reason = reason
            trans.amount_completed = 0
        if litre:
            trans.amount_completed = int(litre * 100)
        trans.dt_end = datetime.today()
        self.__session.merge(trans)
        self.__session.commit()
