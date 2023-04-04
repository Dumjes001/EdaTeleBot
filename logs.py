import logging


def get_mini_logs():
    logs = logging.basicConfig(filename="error.log", level=logging.ERROR)
    return logs


def get_maxi_logs(logger):
    # create a logger
    logger = logging.getLogger(__name__)

    # set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.INFO)

    # create a file handler and set the logging level
    file_handler = logging.FileHandler("bot.log")
    file_handler.setLevel(logging.INFO)

    # create a formatter and add it to the handler
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler.setFormatter(formatter)

    # add the handler to the logger
    logger.addHandler(file_handler)
