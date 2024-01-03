from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from dnschecker.api.dns import create_dns_routes
import time
import logging
import asyncio
from dnschecker.api.deps import dns_resolver_dep

# Initialize a FastAPI application instance
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) with specific configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials to be included in the requests
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Configure logger for the application
logger = logging.getLogger(__name__)

# Create and add DNS routes to the FastAPI app
create_dns_routes(app)

# Middleware to log requests and add a custom header for process time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # Log request details except for health check endpoint
    if not request.base_url == '/healthcheck':
        logger.info(f'request: {request.base_url} {request.url} {request.url.path} {request.url.components}')

    # Measure request processing time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # Add custom header with process time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Event handler for app startup
@app.on_event('startup')
async def startup_event():
    # Set logger level
    logger.setLevel('INFO')

    # Initialize DNS resolver dependency
    loop = asyncio.get_running_loop()
    logger.info('Init DNS Resolver')
    await dns_resolver_dep.init(loop)
    logger.info('DNS Resolver inited')

# Health check endpoint
@app.get('/healthcheck')
def healthcheck():
    return 'OK'

# Mount static files and DNS API routes
app.mount('/api/dns', dns_api)  # Mount API routes under '/api/dns'
app.mount('/dns', StaticFiles(directory="/app/static", html=True), name="frontend")  # Serve static files for frontend
