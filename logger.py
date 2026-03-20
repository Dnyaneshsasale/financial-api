import logging

logging.basicConfig(
    filename="app.log",   # log file name
    level=logging.INFO,   # what to track
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()