import logging
import sys


def _init_logger(name: str):
    """Make our custom logger available

    Args:
        name (str): Name of the logger

    Returns:
        Logger: A logger object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # Explicitly set the output of the logger to stdout,
    # this is the default stream for normal program output.
    # By default, it is redirected to terminal
    handler = logging.StreamHandler(sys.stdout)
    # Format the log message
    formatter = logging.Formatter(
        '%(levelname)s:     %(name)s:%(module)s - "%(message)s"',
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    # Add the handler to the logger
    logger.addHandler(handler)
    return logger


# Initialize the logger
logger = _init_logger(name="hpp-logger")
