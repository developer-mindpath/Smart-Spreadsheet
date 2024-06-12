import logging

logging.basicConfig(
    level=logging.INFO,
    format='\033[0;32m%(levelname)s\033[0m:\t  %(asctime)s\t %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger()
