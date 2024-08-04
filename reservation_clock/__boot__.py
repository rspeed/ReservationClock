import logging
from sys import stdout
from micropython import alloc_emergency_exception_buf

from .util.wlan import connect_wlan
from .util.ntp import set_clock


__all__ = 'boot'

logging.basicConfig(level = logging.WARNING, stream = stdout, filename = 'debug.log', filemode = 'w+')

log = logging.getLogger(__name__)



def boot ():
	"""Runs when the controller is powered on."""

	# Allocate a block of memory to store exceptions raised during interrupts
	alloc_emergency_exception_buf(256)

	log.info("Booting…")

	log.info("Connecting to network…")
	connect_wlan()

	log.info("Setting clock…")
	set_clock()

	log.info("Boot complete.")
