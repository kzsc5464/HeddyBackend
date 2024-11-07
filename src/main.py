"""Dummy main for python-project-template."""

import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger()

def dummy():
    """Return Zero Dummy"""
    return 0

if __name__ == "__main__":  # pragma: no cover
    logger.critical("Critical Msg")
    logger.error("Error Msg")
    logger.warning("Warning Msg")
    logger.info("Info Msg")
    logger.debug("Debug Msg")