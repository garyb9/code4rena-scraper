import sys
import json
import logging
import asyncio

from bs4 import BeautifulSoup
from scraper import download_page, get_dynamic_links, get_links_in_page_async
from setup_env import setup
from consts import AUDITS_MAIN_PAGE

setup()
logger = logging.getLogger(__name__)


async def main() -> None:
    page = await get_dynamic_links(AUDITS_MAIN_PAGE)

    if not page:
        print("Failed to retrieve the page.")
        return

    links = await get_links_in_page_async(page)
    audit_links_filtered = sorted(
        [link for link in links if "/audits/" in link], reverse=True
    )
    logger.info(json.dumps(list(audit_links_filtered), indent=4))


# Run
if __name__ == "__main__":
    try:
        logging.info("Application running - Press Ctrl+C to exit.")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Application interrupted. Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        logging.info("Application has been shut down")
        sys.exit(0)
