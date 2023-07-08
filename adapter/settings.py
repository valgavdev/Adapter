import os
from typing import Optional

import settingsbase
import basedb
from .api.ts94 import ConnectionInfo

DEFAULT_CFG = os.path.dirname(__file__) + '/adapter.cfg'


class Settings(settingsbase.SettingsBase):
    def __init__(self, cfg_file: str = DEFAULT_CFG, encoding: str = None):
        self.__db_sets = None

        super().__init__(cfg_file if cfg_file else DEFAULT_CFG, encoding=encoding)

    def read(self):
        def read_conection_info(section: str, default: basedb.ConnectionInfo = basedb.ConnectionInfo()) \
                -> basedb.ConnectionInfo:
            pwd = self.get_encrypt(section, 'password')
            if not pwd:
                pwd = default.password
            return basedb.ConnectionInfo(server=self.get(section, 'server', default=default.server),
                                         dbname=self.get(section, 'name', default=default.dbname),
                                         user=self.get(section, 'user', default=default.user),
                                         password=pwd)

        super().read()

        self.__db_sets = read_conection_info('DB')

    def get_db_sets(self) -> basedb.ConnectionInfo:
        return self.__db_sets

    def get_ts94_sets(self) -> Optional[ConnectionInfo]:
        connection_info = ConnectionInfo(url=self.get('TS94', 'url'),
                                         login=self.get('TS94', 'login'),
                                         password=self.get('TS94', 'password'))
        if not connection_info.url or not connection_info.login or not connection_info.password:
            return None

        return connection_info
