from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger, handlers

# Setup default logger of the application.
logger_default = getLogger("logger_default")
logger_default.setLevel(DEBUG)
log_fmt = Formatter("%(asctime)s - %(process)d - %(levelname)s - %(message)s")

# Setup log handler - to console.
log_c_handler = StreamHandler()
log_c_handler.setFormatter(log_fmt)
logger_default.addHandler(log_c_handler)

# Setup log handler - to file (5MB per each log file).
log_f_handler = handlers.RotatingFileHandler("corsearch.log", maxBytes=5120000, backupCount=5)
log_f_handler.setFormatter(log_fmt)
logger_default.addHandler(log_f_handler)


def log_debug(msg: str, logger: Logger = logger_default):
    """Wrapper function for debug logging.

    Args:
        msg: Message to log.
        logger: Specify logger object.
    """
    logger.debug(msg)


def log_info(msg: str, logger: Logger = logger_default):
    """Wrapper function for info logging.

    Args:
         msg: Message to log.
         logger: Specify logger object.
    """
    logger.info(msg)


def log_warning(msg: str, logger: Logger = logger_default):
    """Wrapper function for warning logging.

    Args:
         msg: Message to log.
         logger: Specify logger object.
    """
    logger.warning(msg)


def log_error(msg: str, logger: Logger = logger_default):
    """Wrapper function for error logging.

    Args:
         msg: Message to log.
         logger: Specify logger object.
    """
    logger.error(msg)


def log_critical(msg: str, logger: Logger = logger_default):
    """Wrapper function for critical logging.

    Args:
         msg: Message to log.
         logger: Specify logger object.
    """
    logger.critical(msg)
