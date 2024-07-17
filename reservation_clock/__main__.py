import ntptime
import logging

from sys import stdout
from time import sleep
from micropython import alloc_emergency_exception_buf

from reservation_clock.wlan import connect_wlan
from reservation_clock.reservations import Reservations


__all__ = 'boot', 'main'

logging.basicConfig(level = logging.WARNING, stream = stdout, filename = 'debug.log', filemode = 'w+')

log = logging.getLogger(__name__)



def boot ():
	"""Runs when the controller is powered on."""

	# Allocate a block of memory to store exceptions raised during interrupts
	alloc_emergency_exception_buf(256)

	log.info("Booting…")

	log.info("Connecting to network…")
	connect_wlan()

	# Give the network a moment to settle
	sleep(0.5)

	log.info("Updating clock…")
	try:
		ntptime.timeout = 3
		ntptime.settime()
	except OSError as e:
		log.error("NTP timed out.")
		raise e from e

	log.info("Boot complete.")



def main ():
	"""Starts the application."""

	log.info("Starting the Reservation Clock.")

	Reservations()

	log.info("Reservation Clock started.")



if __name__ == '__main__':
	boot()
	main()
