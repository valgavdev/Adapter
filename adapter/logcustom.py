import logging, re, os, sys  # , platform
from typing import Optional, NamedTuple

# if platform.system() == 'Linux':
#    from systemd import journal

from config import config
from . import requestvars


class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        g = requestvars.g()
        if g:
            val = g.user_id
            if val: record.user_id = val
            val = g.ip
            if val: record.ip = val
            val = g.id
            if val: record.id = val

        arg_pattern = re.compile(r'%\((\w+)\)')
        arg_names = [x.group(1) for x in arg_pattern.finditer(self._fmt)]
        for field in arg_names:
            if field not in record.__dict__:
                record.__dict__[field] = None

        return super().format(record)


class Logger:
    class LogExtra(NamedTuple):
        id: Optional[str] = None
        ip: Optional[str] = None
        user_id: Optional[str] = None

    def __init__(self, logger):
        self.__logger = logger

    def init(self, format_: str, level_=logging.INFO):
        # if platform.system() == 'Linux':
        #    journal_handler = journal.JournaldLogHandler(identifier=config.app_identifier)
        #    journal_handler.setFormatter(CustomFormatter(format_))
        #    self.__logger.addHandler(journal_handler)
        # else:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(CustomFormatter(format_))
        self.__logger.addHandler(stream_handler)

        if config.log_in_file:
            file_handler = logging.FileHandler('{}/adapter.log'.format(os.getcwd()))
            format_ex = '%(asctime)s {}'.format(format_)
            file_handler.setFormatter(CustomFormatter(format_ex, datefmt='%Y-%m-%d %H:%M:%S'))
            self.__logger.addHandler(file_handler)

        self.__logger.setLevel(level_)

    def logger(self):
        return self.__logger

    def __write(self, message, level=logging.INFO, extra: LogExtra = LogExtra()):
        self.__logger.log(level, message, extra={'id': extra.id,
                                                 'ip': extra.ip,
                                                 'user_id': extra.user_id})

    def debug(self, message, extra: LogExtra = LogExtra()):
        self.__write(message, level=logging.DEBUG, extra=extra)

    def info(self, message, extra: LogExtra = LogExtra()):
        self.__write(message, level=logging.INFO, extra=extra)

    def error(self, message, extra: LogExtra = LogExtra()):
        self.__write(message, level=logging.ERROR, extra=extra)

    def exception(self, message, extra: LogExtra = LogExtra()):
        if config.log_exception:
            self.__logger.exception(message)
        self.error(message, extra=extra)
