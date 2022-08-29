import asyncio
import logging
import os

import httpx
from fastapi import FastAPI, Request, Response

PROXY = os.getenv('HTTP_PROXY', None)
PROXY_URL = os.getenv('PROXY_URL', 'https://api.telegram.org')
TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', 5))
DEBUG = os.getenv('DEBUG', None)

if PROXY_URL and PROXY_URL[-1] == '/':
    PROXY_URL = PROXY_URL[:-1]

logger = logging.getLogger('uvicorn.debug')
if DEBUG:
    logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.route("/{full_path:path}", methods=['GET', 'POST', 'HEAD'])
async def proxy_request_to_proxy(request: Request):
    method = request.method

    full_path = request.path_params['full_path']

    headers = dict(request.headers)
    headers.pop('host')
    headers.pop('user-agent')

    content = await request.body()

    logger.debug(PROXY)
    logger.debug(TIMEOUT_SECONDS)
    logger.debug(PROXY_URL)
    logger.debug(full_path)
    logger.debug(headers)
    logger.debug(method)
    logger.debug(content)

    async with httpx.AsyncClient(proxies=PROXY, headers=headers, timeout=TIMEOUT_SECONDS) as client:
        result = await asyncio.gather(client.request(method, f'{PROXY_URL}/{full_path}', content=content))
        response = result[0]

    logger.debug(response.content)
    logger.debug(response.status_code)
    logger.debug(response.headers)

    return Response(response.content, response.status_code, response.headers)
