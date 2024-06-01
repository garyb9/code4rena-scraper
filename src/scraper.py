import asyncio
import logging
import random
import time
import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_links_in_page_async(page: Page) -> list:
    """The function returns a set of links (strings) in the given page"""
    soup = BeautifulSoup(page.content, "lxml")
    links = set(a_tag["href"] for a_tag in soup.find_all("a", href=True))
    return list(links)


async def get_dynamic_links(url: str) -> Page:
    """Fetch the page content from a dynamically loaded page using Selenium"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    try:
        driver.get(url)
        # Example of waiting for a specific element
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        # Introducing a random delay
        time.sleep(random.uniform(2, 5))
        content = driver.page_source
        return Page(url=url, content=content)
    finally:
        driver.quit()
