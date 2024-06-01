import os
import sys
import time
import random
import logging
from dotenv import load_dotenv


def setup():
    # Setup environment variables
    load_dotenv(
        dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
    )

    # Set up logger
    logging.basicConfig(
        format="%(asctime)s:%(msecs)d\t%(name)s:\t%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(
                sys.stdout
            )  # Ensure log messages are printed to the console
        ],
        # filename='app.log',  # Log file path
        # filemode='w',  # Append mode (use 'w' for overwrite mode)
    )

    # Seed the random number generator with the current system time
    random.seed(time.time())

    # Set the timezone globally for the os environment
    os.environ["TZ"] = os.getenv("TZ", "Etc/GMT-2")
    if not sys.platform.startswith("win"):
        time.tzset()
