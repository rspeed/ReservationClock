from sys import stdout
from logging import basicConfig, getLogger as get_logger, DEBUG


__all__ = 'get_logger'

basicConfig(level = DEBUG, stream = stdout)
