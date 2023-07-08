from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    celery_off: bool = False
    log_exception: bool = True
    log_in_file: bool = False
    common_lib: str = '/home/user_api/elsyplusapi/common'
    config_file: str = '/home/user_api/elsyplusapi/elsyplusapi/elsyplusapi.cfg'
    config_file_encoding: str = 'utf-8'
    celery_broker_url: str = 'redis://127.0.0.1:6379'
    doc: bool = False
