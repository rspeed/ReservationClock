import logging

from reservation_clock.reservations import Reservations


__all__ = 'main'

log = logging.getLogger(__name__)



def main ():
	"""Starts the application."""

	log.info("Starting the Reservation Clock.")

	Reservations()

	log.info("Reservation Clock started.")



if __name__ == '__main__':
	main()
