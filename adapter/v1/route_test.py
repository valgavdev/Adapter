from adapter.logger import http_logger
import time
from fastapi import BackgroundTasks

from . import router_v1


async def task_sample():
    http_logger.info('task work begin')
    time.sleep(10)
    http_logger.info('task work end')


@router_v1.post("/test", tags=['Test'])
def test_background(tasks: BackgroundTasks) -> int:
    tasks.add_task(task_sample)

    return 1
