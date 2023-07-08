from . import prod
from . import debug


class Settings(debug.Settings):
    title: str = 'ADAPTER'
    app_identifier: str = 'adapter'
    db_pool_size: int = 10
    db_use_read: bool = True
    log_format: str = '[LOG %(thread)d][IP=%(ip)s][ID=%(id)s][User=%(user_id)s][%(app_module)s][%(levelname)s]\n\t%(message)s'


config = Settings()
