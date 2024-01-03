from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import time
import logging
import asyncio

from dnschecker.api.deps import dns_resolver_dep
from dnschecker.api.dns import api as dns_api

# 创建 FastAPI 实例
app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

logger = logging.getLogger(__name__)

# 其他路由和事件处理器

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if not request.base_url == '/healthcheck':
        logger.info(f'request: {request.base_url} {request.url} {request.url.path} {request.url.components}')

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.on_event('startup')
async def startup_event():
    logger.setLevel('INFO')

    loop = asyncio.get_running_loop()
    logger.info('Init DNS Resolver')
    await dns_resolver_dep.init(loop)
    logger.info('DNS Resolver inited')

@app.get('/healthcheck')
def healthcheck():
    return 'OK'

app.mount('/api/dns', dns_api)
app.mount('/dns', StaticFiles(directory="/app/static", html=True), name="frontend")
