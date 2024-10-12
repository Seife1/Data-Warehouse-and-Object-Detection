import logging

def setup_logging(log_file='./logs/log.log', level=logging.INFO):
    """
    Sets up logging configuration.

    :param log_file: Path to the log file.
    :param level: Logging level.
    :return: A logger instance.
    """
    logging.basicConfig(
        filename=log_file,
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging is set up.")
    
    return logger
