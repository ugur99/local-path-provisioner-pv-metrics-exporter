import logging

def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    ConsoleOutputHandler = logging.StreamHandler()
    ConsoleOutputHandler.setLevel(logging.DEBUG)
    ConsoleOutputHandler.setFormatter(formatter)

    logger.addHandler(ConsoleOutputHandler)

    return logger
