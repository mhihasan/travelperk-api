from typing import Any

import aiohttp


async def fetch(session: aiohttp.ClientSession, url: str) -> Any:
    async with session.get(url) as response:
        if response.status != 200:
            raise Exception(f"Error on fetching with status: {response.status}")

        return await response.json()
