from fastapi import APIRouter

router_v1 = APIRouter(prefix="/v1")

from . import route_orders
from . import route_config
