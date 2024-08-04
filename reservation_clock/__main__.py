from reservation_clock.reservations import Reservations

from .util.logging import get_logger
from .display import display


__all__ = 'main'

log = get_logger(__name__)



def main ():
	"""Starts the application."""

	log.info("Starting the Reservation Clock.")

	Reservations()

	log.info("Reservation Clock started.")

	log.debug(display)



if __name__ == '__main__':
	main()
