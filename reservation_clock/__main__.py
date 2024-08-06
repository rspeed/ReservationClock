from argparse import ArgumentParser
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

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
	log_level_map = {
		'DEBUG': DEBUG,
		'INFO': INFO,
		'WARNING': WARNING,
		'ERROR': ERROR,
		'CRITICAL': CRITICAL
	}

	parser = ArgumentParser(description = "Runs the Reservation Clock application.")
	# TODO: Add an argument to supply a path to the settings file.
	parser.add_argument('--log-level', default = 'WARNING', help = f"{{{','.join(log_level_map.keys())}}}")
	args = parser.parse_args()

	# Set root logging level
	get_logger().setLevel(log_level_map[args.log_level])

	main()
