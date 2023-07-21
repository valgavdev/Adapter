from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from adapter.logger import http_logger
import time
from fastapi import BackgroundTasks

from . import router_v1
from ..exceptions import CardNotExist


def run_sync_code(task, *args, **kwargs):
    executor = ThreadPoolExecutor()
    loop = get_event_loop()
    loop.run_in_executor(executor, partial(task, *args, **kwargs))


def task_sample(s: str, bo: bool):
    s1 = s
    bo1 = bo
    http_logger.info(f'task work begin: {s1}')
    time.sleep(2)
    http_logger.info('task work end')



@router_v1.post("/test", tags=['Test'])
async def test_background() -> int:
    #d = task_sample()
    http_logger.info('before run')
    run_sync_code(task_sample, 'sdf', True)
    #raise CardNotExist()
    http_logger.info('after run')
    return 1
