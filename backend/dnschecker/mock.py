import time
import traceback

from fastapi import FastAPI, APIRouter
from fastapi import Query, Path, Request

from dnschecker.models import DhtNodeModel, DhtResolveModel
from typing import List, Optional

from loguru import logger


api = FastAPI(docs_url='/')

@api.get('/dhts', response_model=List[DhtNodeModel])
async def get_dhts():
    return [
        DhtNodeModel.parse_obj({'idx': 0, 'ip': '1.2.3.4', 'key': 'abc', 'port': '1111', 'is_online': True}),
        DhtNodeModel.parse_obj({'idx': 1, 'ip': '1.2.3.5', 'key': 'abd', 'port': '2222', 'is_online': False}),
        DhtNodeModel.parse_obj({'idx': 2, 'ip': '1.2.3.6', 'key': 'abe', 'port': '3333', 'is_online': True}),
    ]

@api.post('/dht/{idx}/resolve', response_model=Optional[DhtResolveModel])
async def post_dht_resolve(idx: int=Path(...), adnl: str=Query(...)):
    if idx == 0:
        return DhtResolveModel.parse_obj({'ip': '123.123.123.123', 'port': '9999'})
    if idx == 1:
        return None
    if idx == 2:
        return None


app = FastAPI()
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logger.error(f'request: {request.base_url} {request.url} {request.url.path} {request.url.components}')

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.mount('/api/dns', api)
