from typing import Optional, List

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import create_session
from sqlalchemy import and_

from . import db_engine, Provider, Price, Vw, MapGoods, ProviderInfo


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
