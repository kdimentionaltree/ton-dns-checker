from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

import time
import logging

from dnschecker.api.dns import api as dns_api


logger = logging.getLogger(__name__)


app = FastAPI()
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logger.error(f'request: {request.base_url} {request.url} {request.url.path} {request.url.components}')

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.mount('/api/dns', dns_api)
app.mount('/dns', StaticFiles(directory="/app/static", html=True), name="frontend")
