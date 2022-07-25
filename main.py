import asyncio
import os

import httpx
from fastapi import FastAPI, Request, Response

PROXY = os.getenv('HTTP_PROXY', None)
PROXY_URL = os.getenv('PROXY_URL', 'https://api.telegram.org')
TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', 5))

if PROXY_URL and PROXY_URL[-1] == '/':
    PROXY_URL = PROXY_URL[:-1]

app = FastAPI()


@app.route("/{full_path:path}", methods=['GET', 'POST', 'HEAD'])
async def proxy_request_to_proxy(request: Request):
    method = request.method

    full_path = request.path_params['full_path']

    headers = dict(request.headers)
    headers.pop('host')
    headers.pop('user-agent')

    content = await request.body()

    async with httpx.AsyncClient(proxies=PROXY, headers=headers, timeout=TIMEOUT_SECONDS) as client:
        result = await asyncio.gather(client.request(method, f'{PROXY_URL}/{full_path}', content=content))
        response = result[0]
    return Response(response.content, response.status_code, response.headers)
