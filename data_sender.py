import asyncio
import os

import httpx

from expenses_fetcher.variables import BUDGET_MAINTAINER_URL


async def store_data(data: list) -> str:
    url = os.path.join(BUDGET_MAINTAINER_URL, 'api', 'operations')
    async with httpx.AsyncClient() as c:
        tasks = [c.post(url, json=operation) for operation in data]
        reqs = await asyncio.gather(*tasks)

    if all([req.status_code == 200 for req in reqs]):
        return ""
    else:
        errs = f"errors: {'; '.join([f'{req.url} {req.status_code}:{req.reason_phrase}' for req in reqs if req.status_code != 200])}"
        return errs
