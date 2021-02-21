import logging


def get_logger():
    log = logging.getLogger()

    console = logging.StreamHandler()

    format_str = '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'
    console.setFormatter(logging.Formatter(format_str))

    if log.hasHandlers():
        log.handlers.clear()

    log.addHandler(console)
    log.setLevel(logging.INFO)

    return log
