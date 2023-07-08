from sqlalchemy import create_engine

from config import config
from .settings import Settings


def create_settings() -> Settings:
    sets = Settings(config.config_file, encoding=config.config_file_encoding)
    sets.read()

    return sets


def create_db(sets: Settings):
    con_info = sets.get_db_sets()

    return create_engine("postgresql+psycopg2://{}:{}@{}/{}".format(con_info.user,
                                                                    con_info.password,
                                                                    con_info.server,
                                                                    con_info.dbname))
