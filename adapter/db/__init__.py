from sqlalchemy import Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import Table, MetaData, Column

from adapter import maker, app_sets

db_engine = maker.create_db(app_sets)
Base = declarative_base()
metadata = MetaData()
metadata.reflect(bind=db_engine)


class IView(object):
    def as_dict(self):
        return [getattr(self, c.name) for c in self.__table__.columns]


class Provider(Base, IView):
    __table__ = Table('provider', metadata, autoload=True)


# class Price(Base, IView):
#     __table__ = Table('station_price', metadata, autoload=True)
class ProviderInfo(Base, IView):
    __table__ = Table('_vw_providers', metadata, Column("id", Integer, primary_key=True), autoload_with=db_engine)


class Price(Base, IView):
    __table__ = Table('_vw_station_prices', metadata, Column("id", Integer, primary_key=True), autoload_with=db_engine)


class Vw(Base, IView):
    __table__ = Table('_vw_stations_config', metadata, Column("id", Integer, primary_key=True), autoload_with=db_engine)


class MapGoods(Base, IView):
    __table__ = Table('map_goods', metadata, autoload=True)