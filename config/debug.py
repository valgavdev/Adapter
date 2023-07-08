from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    log_exception: bool = True 
    log_in_file: bool = True    
    config_file: str = None
    common_lib: str = None
    config_file_encoding: str = 'utf-8'    
    doc: bool = True
