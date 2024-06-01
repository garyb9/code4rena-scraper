import re
import sys
import asyncio
import logging
import aiohttp
from typing import Set
from bs4 import BeautifulSoup


class Page:
    def __init__(self, url: str, content: str):
        """
        Initialize a new Page instance.

        :param url: The URL of the web page.
        :param content: The content of the web page, typically HTML.
        """
        self.url = url
        self.content = content


async def download_page(
    url: str, max_retries: int = 3, timeout_seconds: int = 10
) -> Page:
    """The function returns an instance of a Page object, with retry and timeout implemented"""
    retries = 0
    while retries < max_retries:
        try:
            timeout = aiohttp.ClientTimeout(total=timeout_seconds)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()  # Raises an error for 4xx/5xx status
                    content = await response.text()
                    return Page(url=url, content=content)
        except Exception as e:
            logging.error(
                f"Error downloading {url} (Attempt {retries + 1}/{max_retries}): {e}"
            )
            retries += 1
            if retries >= max_retries:
                logging.error(f"Failed to download {url} after {max_retries} attempts.")
                return None
            await asyncio.sleep(1)  # Wait a bit before retrying
