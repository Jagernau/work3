import logging


def api_log_info(argument):
    """логгер принимающий логги сразу в info"""
    logger = logging.getLogger("basic")
    logger.setLevel("DEBUG")

    file_handler = logging.FileHandler("./logs/api.log")
    logger.addHandler(file_handler)
    formater = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formater)

    logger.info(argument)

