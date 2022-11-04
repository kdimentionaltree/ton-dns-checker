import time
import traceback

from fastapi import FastAPI
from fastapi import Query, Path, Request

from dnschecker.schemas.models import DhtNodeModel, DhtResolveModel
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


@api.get('/resolve', response_model=List[DhtResolveModel])
async def get_resolve(adnl: str=Query(...)):
    return [
        DhtResolveModel.parse_obj({'ip': '123.123.123.123', 'port': '7777'}),
        DhtResolveModel.parse_obj({}),
        DhtResolveModel.parse_obj({'ip': '123.123.123.123', 'port': '9999'}),
    ]


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
