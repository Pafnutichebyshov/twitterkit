import logging


def getLogger(name, log_level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    fh = logging.FileHandler('{}.log'.format(name))
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
