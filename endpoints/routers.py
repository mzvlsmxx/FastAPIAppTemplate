from fastapi import APIRouter

from endpoints.root import router as router_root
from endpoints.service import router as router_service

routers: list[APIRouter] = [router_root, router_service]
