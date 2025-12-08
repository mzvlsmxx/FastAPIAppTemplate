from fastapi import APIRouter

from endpoints.root import router as router_root
from endpoints.data import router as router_endpoints

routers: list[APIRouter] = [router_root, router_endpoints]
