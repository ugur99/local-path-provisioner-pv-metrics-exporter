import logging, os

def get_logger():
    logger = logging.getLogger(__name__)

    try:
        os.environ["LOG_LEVEL"]
    except KeyError:
        logger.warning("LOG_LEVEL was not set, defaulting to INFO")
        logLevel = "INFO"
    else:
        logLevel = os.environ["LOG_LEVEL"].upper()

    logger.setLevel(logging.getLevelName(logLevel))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    ConsoleOutputHandler = logging.StreamHandler()
    ConsoleOutputHandler.setLevel(logging.DEBUG)
    ConsoleOutputHandler.setFormatter(formatter)

    logger.addHandler(ConsoleOutputHandler)

    return logger
