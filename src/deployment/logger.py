import logging

def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    #handler = logging.FileHandler('logger.log')
    #handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    #handler.setFormatter(formatter)

    ConsoleOutputHandler = logging.StreamHandler()
    ConsoleOutputHandler.setLevel(logging.DEBUG)
    ConsoleOutputHandler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ConsoleOutputHandler)
    #logger.addHandler(handler)

    return logger
